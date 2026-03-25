1. **What object type is this?** String, list, dict, Series, DataFrame, datetime, object?
2. **Mutates or returns a new value?** `"book-book".replace("book", "novel", 1)` returns a **new string**; `items.append(x)` mutates the list and returns `None`.
3. **Labels or positions?** Pandas: `df.loc[2, 'B']` uses labels; `df.iloc[1, 1]` uses integer positions.
4. **Value shape?** `df['B']` -> Series, `df[['B']]` -> DataFrame.
5. **Method or free function?** `"Amsterdam".count('a')`, not `count("Amsterdam", 'a')`.
6. **Did they reassign?** If not, immutable objects such as strings stay unchanged.
7. **Scope okay?** A name created inside a function cannot be used outside it.
8. **Parse or format?** `datetime.strptime("03-02-2013", "%d-%m-%Y")` reads a string; `dt.strftime("%d-%m-%Y")` writes a string.
9. **Stop exclusive?** `x[1:4]` uses indices `1,2,3`; the stop index is excluded.
10. **Could the answer simply be an error?** Many distractors fail before any deeper logic matters.
