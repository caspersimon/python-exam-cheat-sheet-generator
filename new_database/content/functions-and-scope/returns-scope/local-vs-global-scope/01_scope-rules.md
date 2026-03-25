| Situation | Result |
|---|---|
| Name created inside function | local to that function |
| Name created outside function | global/module-level |
| Read global inside function, no assignment | allowed |
| Assign to a name inside function | Python treats that name as local unless `global` is used |
| Use local name outside function | `NameError` |
