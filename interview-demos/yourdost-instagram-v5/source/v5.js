/* YourDOST v5: two story-style posts modelled on the reference carousels (TailCrafts, @therapeuticallyours):
   candid photos cut out as stickers, handwritten notes, hand-drawn doodles, YourDOST logo on every slide. */
(function (root) {
  "use strict";
  const Y = "#f6d25a";
  const badge = `<img class="badge" src="brand/badge.png" alt="YourDOST">`;
  const CTA = `<div class="cta">Talk to a certified expert, 24/7 · <b>yourdost.com</b></div>`;

  // hand-drawn doodles
  const D = {
    loop: (c = "#fff", w = 220, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 220 200" width="${w}"><path d="M150 30 C 60 0 10 80 60 130 C 110 180 200 140 180 80 C 165 35 90 40 80 90 C 72 130 130 150 160 120" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round"/></svg>`,
    arrow: (c = Y, w = 200, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 200 60" width="${w}"><path d="M8 34 C 60 28 120 30 182 26" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round"/><path d="M160 8 L186 26 L162 46" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    curvy: (c = Y, w = 220, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 220 160" width="${w}"><path d="M14 20 C 40 120 120 140 186 120" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round"/><path d="M164 96 L190 120 L162 140" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    burst: (c = "#fff", w = 120, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 120 120" width="${w}"><path d="M20 70 L52 84 M30 30 L60 62 M76 14 L78 56" stroke="${c}" stroke-width="8" stroke-linecap="round"/></svg>`,
    wavy: (c = "#fff", w = 520, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 520 30" width="${w}"><path d="M4 16 Q 30 2 56 16 T 108 16 T 160 16 T 212 16 T 264 16 T 316 16 T 368 16 T 420 16 T 472 16 T 516 16" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round"/></svg>`,
    heart: (c = "#fff", w = 150, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 150 140" width="${w}"><path d="M75 128 C 20 90 6 60 14 36 C 24 8 62 8 75 40 C 88 8 128 8 136 36 C 144 62 128 92 75 128 Z" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    sparkle: (c = Y, w = 70, st = "") => `<svg class="doodle" style="${st}" viewBox="0 0 70 70" width="${w}"><path d="M35 4 L41 29 L66 35 L41 41 L35 66 L29 41 L4 35 L29 29 Z" fill="${c}"/></svg>`,
  };

  const story = (img, label) => `<div class="story"><div class="ring"><img src="photos/${img}.jpg" alt=""></div><span>${label}</span></div>`;

  const POSTS = [
    {
      id: "11", slug: "Carousel-First-Semester", kind: "carousel", segment: "College students, especially first-years who moved cities for college",
      date: "Mon 30 Nov 2026", time: "8:00 PM IST", theme: "Homesickness in the first semester",
      line: "Nobody tells you how the first semester feels.",
      why: "It tells a story across the swipe like the reference posts: a candid student walking into campus, the 2 AM comparison spiral, then a reframe students can repeat to themselves. The last slide tells them they may already have YourDOST through college.",
      slides: [
        () => `<div class="ph" style="background-image:url(photos/campus-road.jpg)"></div><div class="shade-top"></div>
          <div class="abs" style="left:70px;right:70px;top:150px"><p class="hl" style="color:${Y};font-size:86px">Nobody tells you how the first semester feels.</p>
          <p class="note" style="color:#fff;margin-top:24px">(swipe if you just moved for college)</p></div>
          <img class="sticker" src="cutouts/student-walking.png" style="left:330px;bottom:-30px;height:820px;transform:rotate(-2deg)">
          ${D.loop("#fff", 200, "left:640px;top:600px;transform:rotate(12deg)")}
          ${D.arrow(Y, 210, "right:60px;bottom:110px")}${badge}`,
        () => `<div class="paper purple"></div>
          <div class="abs" style="left:70px;right:330px;top:150px"><p class="hl" style="color:${Y}">New city.<br>New hostel.<br>300 new faces.</p>${D.wavy("#fff", 470, "position:relative;margin-top:6px")}</div>
          <div class="circle" style="right:60px;top:170px;width:260px;height:260px"><img src="photos/walkway.jpg" alt=""></div>
          <img class="sticker" src="cutouts/backpack.png" style="left:110px;bottom:60px;height:560px;transform:rotate(-7deg)">
          ${D.burst("#fff", 120, "left:70px;top:740px")}
          <div class="abs" style="left:560px;right:50px;top:700px"><p class="note" style="color:#fff">everyone seems to have it all figured out…</p><p class="note" style="color:${Y};font-size:64px;margin-top:20px">but…</p>${D.arrow(Y, 200, "position:relative;margin-top:6px")}</div>${badge}`,
        () => `<div class="paper cream"></div>
          <div class="abs" style="left:70px;right:70px;top:150px"><p class="hl dark">At 2 AM, you watch everyone's <span class="mk">“best week ever”</span> stories.</p></div>
          <div class="stories" style="top:560px">${story("story-fest", "fest night!!")}${story("story-beach", "beach trip")}${story("story-chai", "new gang")}</div>
          <div class="abs" style="left:70px;right:70px;top:1000px"><p class="note dark" style="text-align:center">(and wonder why yours doesn't look like that)</p></div>
          ${D.sparkle(Y, 70, "right:70px;top:500px")}${D.sparkle("#c9b6f2", 46, "left:80px;top:520px")}${badge}`,
        () => `<div class="ph" style="background-image:url(photos/rain-window.jpg)"></div><div class="shade-all"></div>
          <div class="abs" style="left:70px;right:70px;top:330px"><p class="hl" style="color:#fff">Homesick isn't weakness.</p><p class="hl" style="color:${Y};margin-top:26px">It means you have a home worth missing.</p></div>
          ${D.heart("#fff", 150, "right:110px;top:820px;transform:rotate(-10deg)")}${badge}`,
        () => `<div class="paper yellow"></div>
          <div class="abs" style="left:70px;right:70px;top:190px"><p class="hl dark" style="font-size:92px">You don't have to figure it out alone.</p>
          <p class="body" style="margin-top:34px">Many colleges already give students access to YourDOST. Check your college email, then talk to someone, any time.</p>
          <div style="margin-top:40px">${CTA}</div>
          <p class="note dark" style="margin-top:70px">send this to your hostel group chat</p>${D.curvy("#141416", 190, "position:relative;margin-left:420px;margin-top:-20px")}</div>${badge}`,
      ],
      caption: "Nobody tells you how the first semester actually feels. 🎒\n\nNew city, new hostel, new everything. And at 2 AM, everyone else's stories make it look easy.\n\nHomesick isn't weakness. It means you have a home worth missing. If it's getting heavy, many colleges already give students access to YourDOST: check your college email.",
      tags: "#FirstSemester #Homesick #CollegeLife #HostelLife #StudentMentalHealth #YourDOST",
      first: "Tag your hostel roommate. 💛 Or tell us: how long did it take you to settle in?",
      alt: [
        "A student with a backpack, seen from behind, walking down a tree-lined college road. Text: Nobody tells you how the first semester feels. Swipe if you just moved for college.",
        "A backpack and a small photo of a college walkway on purple. Text: New city. New hostel. 300 new faces. Everyone seems to have it all figured out… but…",
        "Three Instagram-style story circles: fest night, beach trip, new gang. Text: At 2 AM, you watch everyone's best week ever stories (and wonder why yours doesn't look like that).",
        "Rain on a window at dusk. Text: Homesick isn't weakness. It means you have a home worth missing.",
        "Text on yellow: You don't have to figure it out alone. Many colleges already give students access to YourDOST. Check your college email. Talk to a certified expert, 24/7. Send this to your hostel group chat.",
      ],
    },
    {
      id: "12", slug: "Image-Weekend-Off", kind: "single", segment: "Working professionals and employees at YourDOST's corporate clients",
      date: "Sun 6 Dec 2026", time: "6:00 PM IST", theme: "Always-on work culture",
      line: "You promised yourself one weekend off.",
      why: "Posted at 6 PM on a Sunday, the exact moment it describes. The phone with a “quick one” work email is something every employee has held; the last line gives them permission to rest.",
      slides: [
        () => `<div class="paper cream"></div>
          <div class="abs" style="left:70px;right:380px;top:140px"><p class="hl dark" style="font-size:84px">You promised yourself one weekend off.</p></div>
          <div class="phone" style="right:-30px;top:330px;width:660px">
            <img class="sticker" src="cutouts/phone-hands.png" style="position:relative;width:100%">
            <div class="lock" style="left:52%;top:9%;transform:rotate(13deg)">Sun 6:14</div>
            <div class="notif" style="left:43%;top:17%;width:42%;transform:rotate(13deg)"><b><i class="mail"></i>Work email · now</b><strong>Quick one before Monday?</strong><span>Can you just check this tonight…</span></div>
          </div>
          <div class="abs" style="left:70px;width:400px;top:560px"><p class="note dark">“just one quick check”</p>${D.arrow("#5b4a9c", 200, "position:relative;margin-top:10px")}<p class="note" style="color:#5b4a9c;margin-top:36px">(3 hours later…)</p></div>
          <div class="band"><div class="abs" style="left:70px;right:70px;top:34px"><p class="hl" style="color:#4c3d8f;font-size:64px;text-shadow:none">Rest isn't a reward for finishing everything.</p><div style="margin-top:22px">${CTA}</div></div></div><img class="badge" src="brand/badge.png" alt="YourDOST" style="left:auto;right:64px;bottom:64px;transform:none;width:120px;height:120px">`,
      ],
      caption: "Be honest: how many times did you check work email this weekend? 📱\n\nRest isn't a reward for finishing everything. It's what lets you keep going.\n\nIf work never really switches off, talk to someone. Your company may already offer YourDOST: ask HR.",
      tags: "#WorkLifeBalance #Burnout #SundayScaries #MentalHealthAtWork #EmployeeWellbeing #YourDOST",
      first: "Drop the number of times you checked work email this weekend. No judgement. 👇",
      alt: ["Hands holding a phone showing Sunday 6:14 and a work email notification: Quick one before Monday? Can you just check this tonight… Text: You promised yourself one weekend off. Just one quick check (3 hours later…). Rest isn't a reward for finishing everything. Talk to a certified expert, 24/7."],
    },
  ];

  function frame(post, i = 0) { return `<div class="f">${post.slides[i]()}</div>`; }
  root.YD5 = { POSTS, frame };
})(typeof window !== "undefined" ? window : globalThis);
