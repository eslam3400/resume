// Résumé layout — reads all content from resume.yaml in this same folder.
// Compile in the free Typst web app: https://typst.app
// Upload resume.typ and resume.yaml together, then export as PDF.
// No compiler binary and no Python needed for the PDF.

#let data = yaml("resume.yaml")

#let navy = rgb("#172d45")
#let amber = rgb("#a86717")
#let muted = rgb("#526173")
#let hairline = rgb("#d9dfe4")

#set page(paper: "a4", margin: (top: 16mm, bottom: 16mm, left: 17mm, right: 17mm))
#set text(font: ("Arial", "Helvetica", "Libertinus Sans"), size: 10pt, fill: navy)
#set par(leading: 0.55em, justify: false)
#show link: set text(fill: navy)

#let section(title) = {
  v(7pt)
  text(size: 9pt, weight: "bold", fill: amber, tracking: 1pt)[#upper(title)]
  v(1pt)
  line(length: 100%, stroke: 0.8pt + hairline)
  v(6pt)
}

// ---- Header ----
#text(size: 25pt, weight: "bold", fill: navy)[#data.name]
#text(size: 12pt, fill: muted)[#data.title]
#v(5pt)
#text(size: 8.5pt, fill: navy)[
  #data.location · #link("mailto:" + data.email)[#data.email] ·
  #link("tel:" + data.phone_link)[#data.phone]
]
#v(3pt)
#line(length: 100%, stroke: 1.5pt + amber)
#v(5pt)
#text(size: 8pt, fill: muted, tracking: 1pt)[#upper(data.eyebrow)]
#v(7pt)
#data.intro

// ---- Experience ----
#section("Professional experience")

#set list(marker: text(fill: amber)[•], indent: 11pt, body-indent: 5pt)

#for job in data.experience [
  #block(above: 7pt, below: 5pt)[
    #grid(
      columns: (1fr, auto),
      column-gutter: 8pt,
      text(size: 12pt, weight: "bold", fill: navy)[#job.company],
      text(size: 8.5pt, fill: muted)[#job.dates],
    )
    #text(size: 9.5pt, weight: "bold", fill: navy)[#job.role]
    #text(size: 8.5pt, fill: muted)[ / #job.location]
    #list(..job.bullets.map(b => [#b]))
  ]
]

// ---- Skills ----
#section("Technical skills")

#for s in data.skills [
  #text(size: 9.5pt, weight: "bold", fill: navy)[#s.label]: #s.values \
]

// ---- Education ----
#section("Education")

#grid(
  columns: (1fr, auto),
  column-gutter: 8pt,
  [#text(weight: "bold")[#data.education.degree], #data.education.school],
  [#data.education.dates · #data.education.location],
)
