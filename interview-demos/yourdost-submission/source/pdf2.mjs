import { createRequire } from "node:module"; const require=createRequire("/home/user/founders-office-ace/interview-demos/yourdost-instagram-v7/source/");
const { chromium } = require("playwright"); import path from "node:path"; import {pathToFileURL} from "node:url";
const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1600,height:900}});
await p.goto(pathToFileURL(path.resolve("master.html")).href); await p.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))});
await p.pdf({path:"out/master.pdf",width:"1600px",height:"900px",printBackground:true,preferCSSPageSize:true});
for(const [i,el] of (await p.$$('.pg')).entries()) if([1,2,3,4,5,6,7,8,9,10,11,12].includes(i+1)) await el.screenshot({path:`out/n${String(i+1).padStart(2,"0")}.png`});
await b.close();
