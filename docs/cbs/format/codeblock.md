# CBS: `{{codeblock::code}}`

- **Layer:** CBS function
- **Category:** format
- **Aliases:** none
- **Source:** `Refer/Risuai/src/ts/cbs.ts` (`codeblock`)

Renders text as a fenced code block, optionally with a language for syntax
highlighting.

## Syntax

```text
{{codeblock::code}}
{{codeblock::lang::code}}
```

## Arguments

| # | Name | Required | Description |
|---|------|----------|-------------|
| 1 | `lang` | no | A language hint for syntax highlighting. Present only when two or more arguments are given. |
| 2 | `code` | yes | The code to render. This is always the **last** argument. |

## Behavior

The **last** argument is treated as the code and is HTML-escaped (`"` -> `&quot;`,
`'` -> `&#39;`, `<` -> `&lt;`, `>` -> `&gt;`) so it renders literally.

- With a single argument, returns `<pre><code>code</code></pre>`.
- With two or more arguments, the **first** is used as the language and the result
  is `<pre-hljs-placeholder lang="lang">code</pre-hljs-placeholder>`, which Risu's
  renderer later turns into a highlighted block.

Because only the first and last arguments are used, embedding a literal `::`
inside the code splits it into extra arguments; use the
[escaped colon](escaped-characters.md) helper if you need a literal `::`.

## Example

```text
{{codeblock::lua::print("hi")}}
```

renders a Lua-highlighted code block.

## See also

- CBS: [`{{tex}}`](tex.md), [`{{comment}}`](comment.md)
- CBS: [escaped literal characters](escaped-characters.md)
