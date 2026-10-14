# Law: a site in Russia

Present every item as **"a signal or a risk, with a reference to the norm"**. A lawyer gives the verdict;
a check of page code does not replace one. Dates and fine amounts from the 2025–2026 amendments must be
checked against the current text of the law, never quoted from memory. Compiled in October 2026 from a
specialist agent's review, with its own notes on where it was unsure.

If the site clearly targets another jurisdiction, apply that jurisdiction's basics instead and say this
table was not used. For an EU-facing site see item 12.

| # | What to check | How it shows from the outside | Strictness |
|---|---|---|---|
| 1 | Personal data processing policy (152-FZ art. 18.1 p. 2) | `legal.policy_links` in the footer and next to every form; the document answers 200; it names the operator with INN/OGRNIP, purposes, data, retention, a contact for requests | Required if there is a form or an analytics counter. The script checks presence and keywords; whether the text matches reality is for a human |
| 2 | Consent to processing as a separate document (since 01.09.2025) | `A.checks.checkboxes`: not merged with the offer ("I accept the offer and the policy"), not pre-ticked (`checked`), a link to the consent text (`legal.consent_links`). Consent to marketing mailings — a separate checkbox (38-FZ art. 18) | A separate document is required; a pre-ticked box is a violation in the regulator's (Roskomnadzor) view |
| 3 | Notification in the Roskomnadzor register of data operators (art. 22) | INN/OGRNIP from the site (`legal.inn`, `legal.ogrnip`) → search on pd.rkn.gov.ru | Required. Not found → write "no record found", not "not registered" |
| 4 | Data stored in Russia at collection (tightened since 01.07.2025) | Where the form sends data (`action`, browser requests), embedded Google Forms, Typeform, Calendly (`legal.foreign_form_services`) | Required, but only indirect signs are visible from outside. Report as a risk |
| 5 | Foreign services receive the visitor's IP | `legal.foreign_trackers`, third-party hosts: Google Fonts, Analytics, reCAPTCHA, YouTube, Vimeo, Meta pixel | Grey zone (cross-border transfer of an IP alone is unsettled). Good practice: self-host fonts, load videos on click. Flag the Meta pixel separately (Meta is designated extremist in Russia); the consequences for the site are unclear |
| 6 | Yandex Metrica and cookies | `legal.metrika`, `legal.webvisor`; are Metrica and cookies mentioned in the policy | No separate cookie law; a banner is good practice. A mention in the policy is close to required. Webvisor (session recording) on pages with forms is a risk — it records typing |
| 7 | Login via foreign services (149-FZ, since 01.12.2023) | `legal.foreign_login`: Google, Apple; allowed: Gosuslugi, a Russian phone number, the unified biometric system, Russian services | Required. Telegram login widget — the regulator's position is unclear, say exactly that |
| 8 | Seller details (Consumer Protection Law art. 8–9) | Full name of the sole proprietor, OGRNIP, INN, a contact for claims; check OGRNIP on egrul.nalog.ru (not closed) | Required when selling. No details while payments are live is a strong signal |
| 9 | Offer and refunds | A public offer with price, description, terms. `legal.refund_phrases`: "no refunds", "no refund after the first lesson" contradict art. 32 of the Consumer Protection Law (the buyer may cancel at any time, paying actual costs) | Required. The most common and most expensive finding for online schools. Phrases are candidates; a human decides. Diplomas and certificates need a licence; details are unclear |
| 10 | Advertising and promised results | Third-party banners and affiliate links need the "Реклама" label, the advertiser and an `erid` (`legal.erid`). `legal.result_promises`: "guaranteed income", "100 % employment" — risk under 38-FZ art. 5 | Labelling applies only to ads; your own materials about your own course need none. Cannot be told apart automatically — candidates for a human check |
| 11 | Russian language in consumer information (168-FZ, since 01.03.2026) | Buttons and plans only in English ("Sign up", "Pro plan") | Whether it covers websites is unclear. Info or a risk; trademarks do not count |
| 12 | EU (GDPR) | Only if the site clearly targets the EU: prices in euro, an English version, foreign cards. Then: a banner with a real "reject", no analytics before consent | For a typical Russian sole proprietor — "not applicable" |

Wording in the report: "Signal: … Norm: … What to do: … Check with a lawyer: …".
