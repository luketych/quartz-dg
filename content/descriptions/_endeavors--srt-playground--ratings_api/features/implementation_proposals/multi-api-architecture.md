# Multi-API Architecture with Nginx Reverse Proxy

## Overview
Yes, using Nginx as a reverse proxy with Docker containers is the ideal approach. Users access everything through one domain, while internally you have complete flexibility with multiple APIs running on different ports.

## Architecture Diagram
```
User → example.com → Nginx → ├── /api/ratings → FeathersJS (port 3030)
                             ├── /api/cms → Strapi (port 1337)
                             ├── /api/analytics → FeathersJS (port 3031)
                             └── /api/auth → Custom Auth Service (port 4000)
```

## Simple Implementation

### 1. Docker Compose Structure
```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - ratings-api
      - strapi
      - analytics-api
    networks:
      - api-network

  ratings-api:
    build: ./services/ratings-api
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db/ratings
    networks:
      - api-network
    # No exposed ports - only accessible through nginx

  strapi:
    image: strapi/strapi
    environment:
      - DATABASE_CLIENT=postgres
      - DATABASE_HOST=db
    networks:
      - api-network

  analytics-api:
    build: ./services/analytics-api
    networks:
      - api-network

  db:
    image: postgres:14
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - api-network

networks:
  api-network:
    driver: bridge

volumes:
  postgres-data:
```

### 2. Nginx Configuration
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream ratings_api {
        server ratings-api:3030;
    }

    upstream strapi_cms {
        server strapi:1337;
    }

    upstream analytics_api {
        server analytics-api:3031;
    }

    server {
        listen 80;
        server_name example.com;

        # API routing
        location /api/ratings {
            proxy_pass http://ratings_api;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
        }

        location /api/cms {
            rewrite ^/api/cms(.*)$ $1 break;
            proxy_pass http://strapi_cms;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
        }

        location /api/analytics {
            proxy_pass http://analytics_api;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
        }

        # Frontend (if needed)
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }
    }
}
```

## Benefits of This Approach

### 1. **User Simplicity**
- Single domain (example.com)
- Consistent API paths (/api/service-name)
- No CORS issues between services
- Unified SSL certificate

### 2. **Developer Flexibility**
- Each API runs independently
- Can use different frameworks/languages
- Easy to add/remove services
- Services can be updated independently

### 3. **Operational Advantages**
- Centralized logging at nginx level
- Easy rate limiting and security rules
- Load balancing capabilities built-in
- Health checks and circuit breaking

## Simplified Development Setup

### Local Development
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  nginx-dev:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./nginx.dev.conf:/etc/nginx/nginx.conf
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

### Development Nginx Config
```nginx
# nginx.dev.conf - Points to host machine ports
location /api/ratings {
    proxy_pass http://host.docker.internal:3030;
}

location /api/cms {
    proxy_pass http://host.docker.internal:1337;
}
```

This allows running services locally without Docker during development.

## Progressive Implementation

### Phase 1: Start Simple
```bash
# Just two services to start
docker-compose up nginx ratings-api
```

### Phase 2: Add Services
```bash
# Add Strapi when ready
docker-compose up -d strapi
# Nginx automatically picks it up
```

### Phase 3: Production Ready
- Add SSL with Let's Encrypt
- Configure monitoring
- Set up CI/CD per service

## Common Patterns

### 1. Shared Authentication
```nginx
location /api/ {
    # Auth service validates token
    auth_request /api/auth/validate;
    auth_request_set $user_id $upstream_http_x_user_id;
    
    # Pass user info to downstream services
    proxy_set_header X-User-Id $user_id;
}
```

### 2. API Gateway Features
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
}

# Response caching
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=api_cache:10m;

location /api/cms/public {
    proxy_cache api_cache;
    proxy_cache_valid 200 1h;
}
```

### 3. Service Discovery (Advanced)
For dynamic service registration, integrate with Consul:
```nginx
# Using nginx-consul-template
upstream ratings_api {
    {{range service "ratings-api"}}
    server {{.Address}}:{{.Port}};
    {{end}}
}
```

## Quick Start Commands

```bash
# Clone and start
git clone your-repo
cd your-repo
docker-compose up -d

# View logs
docker-compose logs -f nginx

# Add new service
# 1. Add to docker-compose.yml
# 2. Add location block to nginx.conf
# 3. docker-compose up -d new-service

# Access APIs
curl http://localhost/api/ratings/stocks
curl http://localhost/api/cms/content-types
```

## When to Consider Alternatives

This approach works great until you need:
- **Complex routing logic** → Consider Kong or Traefik
- **Service mesh features** → Look at Istio or Linkerd
- **Serverless integration** → AWS API Gateway might be better
- **GraphQL federation** → Apollo Gateway could help

But for most multi-API projects, Nginx + Docker is the sweet spot of simplicity and power.