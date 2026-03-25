1. **What object type is this?** String, list, dict, Series, DataFrame, datetime, object?
2. **Mutates or returns new value?** `str.replace` returns new string; `list.append` mutates and returns `None`.
3. **Labels or positions?** Pandas: `loc` = labels, `iloc` = integer positions.
4. **Value shape?** `df['B']` -> Series, `df[['B']]` -> DataFrame.
5. **Method or free function?** `x.count('a')`, not `count(x, 'a')`.
6. **Did they reassign?** If not, immutable objects stay unchanged.
7. **Scope okay?** Local names die outside function; assigning inside function can shadow globals.
8. **Parse or format?** `strptime` reads string -> datetime. `strftime` writes datetime -> string.
9. **Stop exclusive?** Slices exclude stop index; negative steps reverse direction.
10. **Could the answer simply be “error”?** Many distractors are invalid before any logic matters.
