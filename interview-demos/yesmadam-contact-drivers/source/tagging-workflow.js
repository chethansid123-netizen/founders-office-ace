export const meta = {
  name: 'tag-app-reviews',
  description: 'Double-tag 500 Yes Madam App Store reviews into contact drivers, adjudicate disagreements, and tag 500 Urban Company reviews as a benchmark',
  phases: [
    { title: 'Tag', detail: 'two independent taggers per Yes Madam batch, one per Urban Company batch' },
    { title: 'Adjudicate', detail: 'a third reader settles every primary-driver disagreement' },
  ],
}

const DIR = '/tmp/claude-0/-home-user-founders-office-ace/ae101f53-563e-5879-97d5-92e83c2dbd6d/scratchpad/cdt/batches'

const PRIMARY = ['delay', 'partner_cancellation', 'payment_refund', 'price_clarity', 'service_quality', 'product_fit', 'support', 'app', 'praise', 'other']
const SUBTAGS = [
  'late_arrival', 'slow_assignment', 'service_overran',
  'no_show', 'last_minute_cancel', 'repeated_reschedule', 'no_partner_available',
  'refund_delayed', 'refund_denied', 'charged_not_served', 'wallet_or_coupon_lost', 'payment_failed',
  'hidden_charges', 'offer_not_honoured', 'price_mismatch', 'membership_or_package_confusion',
  'poor_skill', 'rushed_or_incomplete', 'hygiene', 'skin_injury_or_reaction', 'rude_behaviour', 'safety_or_theft',
  'product_quality', 'missing_or_wrong_products', 'product_upsell', 'product_reaction',
  'unreachable', 'unhelpful_or_scripted', 'slow_resolution', 'no_escalation',
  'crash_or_wont_open', 'login_or_otp', 'booking_or_checkout_bug', 'slots_unavailable', 'spam_notifications', 'other_app',
  'praise_professional', 'praise_service', 'praise_value',
  'other_issue', 'unclear',
]
const SERVICES = ['waxing', 'facial_cleanup', 'massage_spa', 'hair', 'mani_pedi', 'threading_bleach', 'laser_advanced', 'makeup', 'multiple', 'unknown']

const CODEBOOK = `
CODEBOOK — contact-driver tagging of app-store reviews for an at-home beauty / home services app (India).
For each review pick ONE primary driver: the problem that made the customer write (the reason they would contact support). Then list any other drivers the review also mentions as secondary.

Primary drivers (use exactly these keys):
- delay: the professional arrived late, assignment took long, or the service overran. Subtags: late_arrival, slow_assignment, service_overran.
- partner_cancellation: the professional did not show up, cancelled late, or the company kept rescheduling / had no professional. Subtags: no_show, last_minute_cancel, repeated_reschedule, no_partner_available.
- payment_refund: money taken or stuck: refund delayed or denied, charged but not served, wallet or coupon money lost, payment failed. Subtags: refund_delayed, refund_denied, charged_not_served, wallet_or_coupon_lost, payment_failed.
- price_clarity: the price or offer was not what was shown: hidden or extra charges at checkout, offers/coupons/free-service promotions that do not work or vanish, price mismatch, membership or package confusion. Subtags: hidden_charges, offer_not_honoured, price_mismatch, membership_or_package_confusion.
- service_quality: the service itself or the professional's conduct: poor skill, rushed or incomplete service, hygiene, a burn/cut/rash caused by technique, rude behaviour, safety or theft. Subtags: poor_skill, rushed_or_incomplete, hygiene, skin_injury_or_reaction, rude_behaviour, safety_or_theft.
- product_fit: the products used: poor or fake-seeming products, products missing or wrong, pushed product upsells, a reaction the customer blames on the product itself. Subtags: product_quality, missing_or_wrong_products, product_upsell, product_reaction.
- support: the complaint is about customer support itself, with no other underlying problem described: unreachable, scripted/unhelpful, slow, no escalation. Subtags: unreachable, unhelpful_or_scripted, slow_resolution, no_escalation.
- app: the app or website: crashes or will not open, login/OTP, booking or checkout bugs (including the professional's app showing different services), no slots shown, spammy notifications. Subtags: crash_or_wont_open, login_or_otp, booking_or_checkout_bug, slots_unavailable, spam_notifications, other_app.
- praise: positive review with no complaint. Subtags: praise_professional, praise_service, praise_value.
- other: complaint that fits none of the above, or too vague to classify (e.g. "worst app", "scam" with no detail). Subtags: other_issue, unclear.

Rules:
1. Support is primary ONLY when support itself is the whole complaint. If the customer describes an underlying problem (refund, no-show, injury...) and then says support did not help, the underlying problem is primary and support is secondary.
2. A burn, rash or cut blamed on the professional's technique = service_quality/skin_injury_or_reaction. Blamed on the product (bad wax, cream) = product_fit/product_reaction. If unclear, use service_quality.
3. "Free pedicure at 1 pm" style offers that vanish, coupons that cannot be used, fake promo notifications = price_clarity/offer_not_honoured. Notification spam with no offer complaint = app/spam_notifications.
4. Paid but booking never happened = payment_refund/charged_not_served. Booking cancelled by them and refund slow = payment_refund/refund_delayed if the refund is the main grievance, else partner_cancellation.
5. A mixed review (praise plus a complaint) gets the complaint as primary. A short vague negative ("worst", "bad service") with no specifics = other/unclear, unless the title gives the specific.
6. Hindi/Hinglish reviews are tagged the same way.

Other fields:
- contacted_support: "yes" if the review says they called, chatted, emailed, raised a ticket or complained to customer care; else "no".
- support_failed: "yes" if they contacted support and say it did not resolve the issue (or was unreachable); else "no".
- severity: "none" for praise; "low" for annoyance; "medium" for a failed or poor service or lost time; "high" for money lost, injury or reaction, harassment, privacy, safety or theft.
- churn_signal: true if they say they will stop using it, uninstall, never book again, or are moving to a competitor.
- service: the service mentioned (${SERVICES.join(', ')}). "unknown" if none.
- city: city if named, else "".
- amount_inr: the most relevant rupee amount mentioned, else 0.
- quote: the 8–25 word verbatim excerpt that best evidences the primary driver. Replace any person's name with [name] and any order id, phone number or email with [id]. Keep the original wording otherwise.
`

const TAGS = {
  type: 'object',
  properties: {
    reviews: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          n: { type: 'integer' },
          primary: { type: 'string', enum: PRIMARY },
          subtag: { type: 'string', enum: SUBTAGS },
          secondary: { type: 'array', items: { type: 'string', enum: PRIMARY } },
          contacted_support: { type: 'string', enum: ['yes', 'no'] },
          support_failed: { type: 'string', enum: ['yes', 'no'] },
          severity: { type: 'string', enum: ['none', 'low', 'medium', 'high'] },
          churn_signal: { type: 'boolean' },
          service: { type: 'string', enum: SERVICES },
          city: { type: 'string' },
          amount_inr: { type: 'number' },
          quote: { type: 'string' },
        },
        required: ['n', 'primary', 'subtag', 'secondary', 'contacted_support', 'support_failed', 'severity', 'churn_signal', 'service', 'city', 'amount_inr', 'quote'],
      },
    },
  },
  required: ['reviews'],
}

const ADJ = {
  type: 'object',
  properties: {
    decisions: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          n: { type: 'integer' },
          primary: { type: 'string', enum: PRIMARY },
          subtag: { type: 'string', enum: SUBTAGS },
          reason: { type: 'string' },
        },
        required: ['n', 'primary', 'subtag', 'reason'],
      },
    },
  },
  required: ['decisions'],
}

const tagPrompt = (file, app, pass) => `You are tagging customer reviews of ${app} from the Apple App Store (India) for a contact-driver analysis.
Read the file ${file}. Each line is one review: "#<n> | <stars>★ | <title> | <text>". There are 100 reviews. Tag EVERY review exactly once, using its n. Do not skip any.
${CODEBOOK}
Work from the review text only. ${pass === 'B' ? 'Tag independently and from scratch; another tagger is tagging the same file and your results will be compared.' : ''}
Return all 100 records.`

function kappa(a, b) {
  const n = a.length
  if (!n) return { n: 0, agree: 0, kappa: 0 }
  let agree = 0
  const ca = {}, cb = {}
  for (let i = 0; i < n; i++) {
    if (a[i] === b[i]) agree++
    ca[a[i]] = (ca[a[i]] || 0) + 1
    cb[b[i]] = (cb[b[i]] || 0) + 1
  }
  const po = agree / n
  let pe = 0
  for (const k of Object.keys(ca)) pe += (ca[k] / n) * ((cb[k] || 0) / n)
  return { n, agree, po, kappa: (po - pe) / (1 - pe) }
}

const YM = [1, 2, 3, 4, 5].map(b => ({ b, file: `${DIR}/ym_${b}.txt` }))
const UC = [1, 2, 3, 4, 5].map(b => ({ b, file: `${DIR}/uc_${b}.txt` }))

const [ymResults, ucResults] = await parallel([
  () => pipeline(
    YM,
    it => parallel([
      () => agent(tagPrompt(it.file, 'Yes Madam (salon at home)', 'A'), { label: `ym${it.b}:A`, phase: 'Tag', schema: TAGS }),
      () => agent(tagPrompt(it.file, 'Yes Madam (salon at home)', 'B'), { label: `ym${it.b}:B`, phase: 'Tag', schema: TAGS }),
    ]),
    ([A, B], it) => {
      const a = A ? A.reviews : [], bb = B ? B.reviews : []
      const bmap = Object.fromEntries(bb.map(r => [r.n, r]))
      const pairs = a.filter(r => bmap[r.n]).map(r => ({ n: r.n, A: r, B: bmap[r.n] }))
      const dis = pairs.filter(p => p.A.primary !== p.B.primary)
      const stats = kappa(pairs.map(p => p.A.primary), pairs.map(p => p.B.primary))
      log(`ym batch ${it.b}: A ${a.length}, B ${bb.length}, primary agreement ${(stats.po * 100).toFixed(0)}% (kappa ${stats.kappa.toFixed(2)}), ${dis.length} to adjudicate`)
      if (!dis.length) return { b: it.b, A: a, B: bb, decisions: [], stats }
      const list = dis.map(p => `#${p.n}: tagger A = ${p.A.primary}/${p.A.subtag}; tagger B = ${p.B.primary}/${p.B.subtag}`).join('\n')
      return agent(`Two taggers disagreed on the primary contact driver for some reviews of Yes Madam. Read the reviews in ${it.file} (lines start with "#<n>"). For each review listed below, apply the codebook strictly and decide the final primary driver and subtag. You may choose a third option if both are wrong. Give a one-line reason.
${CODEBOOK}
DISAGREEMENTS:
${list}`, { label: `ym${it.b}:adjudicate`, phase: 'Adjudicate', schema: ADJ })
        .then(r => ({ b: it.b, A: a, B: bb, decisions: r ? r.decisions : [], stats }))
    }
  ),
  () => pipeline(
    UC,
    it => agent(tagPrompt(it.file, 'Urban Company (home services, incl. salon at home)', 'A'), { label: `uc${it.b}`, phase: 'Tag', schema: TAGS })
      .then(r => ({ b: it.b, reviews: r ? r.reviews : [] }))
  ),
])

const ym = ymResults.filter(Boolean)
const allA = [], allB = []
for (const r of ym) {
  const bmap = Object.fromEntries(r.B.map(x => [x.n, x]))
  for (const x of r.A) if (bmap[x.n]) { allA.push(x.primary); allB.push(bmap[x.n].primary) }
}
const overall = kappa(allA, allB)
log(`Yes Madam overall: ${overall.n} double-tagged, agreement ${(overall.po * 100).toFixed(1)}%, kappa ${overall.kappa.toFixed(2)}`)
return { ym, uc: ucResults.filter(Boolean), overall }
