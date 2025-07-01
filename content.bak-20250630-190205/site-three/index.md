

| A   | B   |
| --- | --- |
| 1   | 2   |


```dataviewjs
const folders = {};

dv.pages()
  .where(p => p.file.path.endsWith(".md"))
  .forEach(p => {
    const folder = p.file.folder;
    if (!folders[folder]) folders[folder] = { count: 0, path: folder };
    folders[folder].count++;
  });

const sortedFolders = Object.entries(folders)
  .sort((a, b) => b[1].count - a[1].count); // change to a[1].path.localeCompare(b[1].path) for alphabetical

dv.table(
  ["📁 Folder", "📄 Files"],
  sortedFolders.map(([_, f]) => [
    dv.fileLink(f.path + "/" + f.path.split("/").pop(), false, f.path), // clickable folder note if it exists
    f.count
  ])
);

```


