// Résumé layout — reads all content from resume.yaml in this same folder.
// Compile in the free Typst web app: https://typst.app
// Upload resume.typ and resume.yaml together, then export as PDF.
// No compiler binary and no Python needed for the PDF.
//
// Roles render two ways, controlled by `detail` in resume.yaml:
//   detail: "full"    -> single-line header + bullets
//   detail: "compact" -> single line in the "Earlier experience" group
// Keep every role in the YAML; only the flags decide what appears on the page.

#let data = yaml("resume.yaml")

#let navy = rgb("#172d45")
#let amber = rgb("#a86717")
#let muted = rgb("#526173")
#let hairline = rgb("#d9dfe4")

#set page(paper: "a4", margin: (top: 12mm, bottom: 10mm, left: 14mm, right: 14mm))
#set text(font: ("Arial", "Helvetica", "Liberation Sans"), size: 9.7pt, fill: navy)
#set par(leading: 0.5em, spacing: 0.5em, justify: false)
#set block(spacing: 0pt)
#show link: set text(fill: navy)

#let section(title) = {
  v(8pt)
  text(size: 8.5pt, weight: "bold", fill: amber, tracking: 1pt)[#upper(title)]
  v(0.5pt)
  line(length: 100%, stroke: 0.8pt + hairline)
  v(5pt)
}

// ---- Header ----
#text(size: 21pt, weight: "bold", fill: navy)[#data.name]
#v(-3pt)
#text(size: 10.5pt, fill: muted)[#data.title]
#v(2pt)
#text(size: 8.5pt, fill: navy)[
  #data.location · #link("mailto:" + data.email)[#data.email] ·
  #link("tel:" + data.phone_link)[#data.phone]
]
#v(1.5pt)
#let profile-links = data.links.map(l => link(l.url)[#l.label]).join([ · ])
#text(size: 8.5pt, fill: navy)[#profile-links]
#v(6pt)
#line(length: 100%, stroke: 1.4pt + amber)
#v(6pt)
#text(size: 7.5pt, fill: muted, tracking: 1pt)[#upper(data.eyebrow)]
#v(5pt)
#text(size: 9.5pt)[#data.intro]

// ---- Experience ----
#let is-full(j) = j.at("detail", default: "full") == "full"
#let full-roles = data.experience.filter(is-full)
#let compact-roles = data.experience.filter(j => not is-full(j))

#section("Professional experience")

#set list(marker: text(fill: amber)[•], indent: 10pt, body-indent: 4pt)
#set list(spacing: 0.42em)

#for job in full-roles [
  #let ps = job.at("positions", default: ())
  #block(above: 16pt, below: 4.5pt)[
    // Company line: name, role (single-position companies), location, dates pinned right.
    #text(size: 11pt, weight: "bold", fill: navy)[#job.company]
    #if ps.len() == 0 [#text(size: 9pt, weight: "bold", fill: navy)[ — #job.role]]
    #text(size: 8.5pt, fill: muted)[ · #job.location]
    #h(1fr)
    #text(size: 8.5pt, fill: muted)[#job.dates]
    // One line per position: indented, its own dates pinned right.
    #for p in ps [
      #linebreak()
      #h(11pt)
      #text(size: 9pt, weight: "bold", fill: navy)[#p.role]
      #h(1fr)
      #text(size: 8.5pt, fill: muted)[#p.dates]
    ]
    // Optional one-line company blurb.
    #if job.at("pref", default: none) != none [
      #linebreak()
      #text(size: 8.5pt, fill: muted, style: "italic")[#job.pref]
    ]
  ]
  #if job.bullets.len() > 0 [
    #list(..job.bullets.map(b => [#b]))
  ]
]

// ---- Earlier experience (compact, one line per role) ----
#section("Earlier experience")

#for (i, job) in compact-roles.enumerate() [
  #grid(
    columns: (1fr, auto),
    column-gutter: 10pt,
    [
      #text(weight: "bold")[#job.company]
      #text(fill: muted)[ — #job.role · #job.location]
    ],
    [#text(size: 8.5pt, fill: muted)[#job.dates]],
  )
  #if i < compact-roles.len() - 1 [ #v(6pt) ]
]

// ---- Skills ----
#section("Technical skills")

#for (i, s) in data.skills.enumerate() [
  #text(size: 9pt, weight: "bold", fill: navy)[#s.label]: #text(size: 9pt)[#s.values]
  #if i < data.skills.len() - 1 [ #v(6pt) ]
]

// ---- Education ----
#section("Education")

#block(above: 0pt, below: 0pt)[#grid(
  columns: (1fr, auto),
  column-gutter: 8pt,
  [#text(weight: "bold")[#data.education.degree], #data.education.school],
  [#data.education.dates · #data.education.location],
)]
