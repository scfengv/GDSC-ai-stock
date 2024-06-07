import{_ as M,o as g,c as p,a,t as _,h as G,v as V,F as E,e as v,b as j,r as R,f as H,w as W}from"./index-CbUvJRks.js";import{C as B,S as U}from"./ScrollReveal-FrL9aeFz.js";/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */const $=Symbol("Comlink.proxy"),Y=Symbol("Comlink.endpoint"),q=Symbol("Comlink.releaseProxy"),P=Symbol("Comlink.finalizer"),b=Symbol("Comlink.thrown"),L=e=>typeof e=="object"&&e!==null||typeof e=="function",X={canHandle:e=>L(e)&&e[$],serialize(e){const{port1:t,port2:n}=new MessageChannel;return F(e,t),[n,[n]]},deserialize(e){return e.start(),I(e)}},Z={canHandle:e=>L(e)&&b in e,serialize({value:e}){let t;return e instanceof Error?t={isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:t={isError:!1,value:e},[t,[]]},deserialize(e){throw e.isError?Object.assign(new Error(e.value.message),e.value):e.value}},A=new Map([["proxy",X],["throw",Z]]);function J(e,t){for(const n of e)if(t===n||n==="*"||n instanceof RegExp&&n.test(t))return!0;return!1}function F(e,t=globalThis,n=["*"]){t.addEventListener("message",function c(r){if(!r||!r.data)return;if(!J(n,r.origin)){console.warn(`Invalid origin '${r.origin}' for comlink proxy`);return}const{id:i,type:o,path:s}=Object.assign({path:[]},r.data),d=(r.data.argumentList||[]).map(h);let l;try{const u=s.slice(0,-1).reduce((m,y)=>m[y],e),f=s.reduce((m,y)=>m[y],e);switch(o){case"GET":l=f;break;case"SET":u[s.slice(-1)[0]]=h(r.data.value),l=!0;break;case"APPLY":l=f.apply(u,d);break;case"CONSTRUCT":{const m=new f(...d);l=re(m)}break;case"ENDPOINT":{const{port1:m,port2:y}=new MessageChannel;F(e,y),l=ne(m,[m])}break;case"RELEASE":l=void 0;break;default:return}}catch(u){l={value:u,[b]:0}}Promise.resolve(l).catch(u=>({value:u,[b]:0})).then(u=>{const[f,m]=S(u);t.postMessage(Object.assign(Object.assign({},f),{id:i}),m),o==="RELEASE"&&(t.removeEventListener("message",c),O(t),P in e&&typeof e[P]=="function"&&e[P]())}).catch(u=>{const[f,m]=S({value:new TypeError("Unserializable return value"),[b]:0});t.postMessage(Object.assign(Object.assign({},f),{id:i}),m)})}),t.start&&t.start()}function K(e){return e.constructor.name==="MessagePort"}function O(e){K(e)&&e.close()}function I(e,t){return T(e,[],t)}function x(e){if(e)throw new Error("Proxy has been released and is not useable")}function z(e){return w(e,{type:"RELEASE"}).then(()=>{O(e)})}const k=new WeakMap,C="FinalizationRegistry"in globalThis&&new FinalizationRegistry(e=>{const t=(k.get(e)||0)-1;k.set(e,t),t===0&&z(e)});function Q(e,t){const n=(k.get(t)||0)+1;k.set(t,n),C&&C.register(e,t,e)}function ee(e){C&&C.unregister(e)}function T(e,t=[],n=function(){}){let c=!1;const r=new Proxy(n,{get(i,o){if(x(c),o===q)return()=>{ee(r),z(e),c=!0};if(o==="then"){if(t.length===0)return{then:()=>r};const s=w(e,{type:"GET",path:t.map(d=>d.toString())}).then(h);return s.then.bind(s)}return T(e,[...t,o])},set(i,o,s){x(c);const[d,l]=S(s);return w(e,{type:"SET",path:[...t,o].map(u=>u.toString()),value:d},l).then(h)},apply(i,o,s){x(c);const d=t[t.length-1];if(d===Y)return w(e,{type:"ENDPOINT"}).then(h);if(d==="bind")return T(e,t.slice(0,-1));const[l,u]=N(s);return w(e,{type:"APPLY",path:t.map(f=>f.toString()),argumentList:l},u).then(h)},construct(i,o){x(c);const[s,d]=N(o);return w(e,{type:"CONSTRUCT",path:t.map(l=>l.toString()),argumentList:s},d).then(h)}});return Q(r,e),r}function te(e){return Array.prototype.concat.apply([],e)}function N(e){const t=e.map(S);return[t.map(n=>n[0]),te(t.map(n=>n[1]))]}const D=new WeakMap;function ne(e,t){return D.set(e,t),e}function re(e){return Object.assign(e,{[$]:!0})}function S(e){for(const[t,n]of A)if(n.canHandle(e)){const[c,r]=n.serialize(e);return[{type:"HANDLER",name:t,value:c},r]}return[{type:"RAW",value:e},D.get(e)||[]]}function h(e){switch(e.type){case"HANDLER":return A.get(e.name).deserialize(e.value);case"RAW":return e.value}}function w(e,t,n){return new Promise(c=>{const r=se();e.addEventListener("message",function i(o){!o.data||!o.data.id||o.data.id!==r||(e.removeEventListener("message",i),c(o.data))}),e.start&&e.start(),e.postMessage(Object.assign({id:r},t),n)})}function se(){return new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-")}const oe={components:{CountTo:B},data(){return{model:{modelName:"",modelFounder:"",output:null,modelGroup:""}}},mounted(){const e=this.$route.path.includes("/News"),t=this.$route.path.includes("/Tweets"),n=this.$route.path.includes("/EarningCall");console.log("isNews:",e),console.log("isTweets:",t),console.log("isEarningCall:",n),e?(this.model.modelName="tesla_news_title_sentiment_analysis",this.model.modelFounder="YC9Z",this.model.modelGroup="News"):t?(this.model.modelName="tweet-sentiment-analysis-for-tesla",this.model.modelFounder="CX330Blake",this.model.modelGroup="Tweets"):n&&(this.model.modelName="tesla_earningscall_sentiment_analysis",this.model.modelFounder="weip9012",this.model.modelGroup="Earnings Call")},computed:{},methods:{async modelInference(){const e=`${this.model.modelFounder}/${this.model.modelName}`,t=this.$refs.textInference.value;console.log(t);const n=new Worker(new URL("/GDSC-ai-stock/assets/model-mLffB-nZ.js",import.meta.url),{type:"module"}),c=I(n);try{const r=await c.fetchData(e,t);this.model.output=r.flat().map(i=>(i.score=Math.round(i.score*1e3)/1e3,i.score=parseFloat(i.score.toFixed(3)),i))}catch(r){console.error(`Error fetching data: ${r}`)}}}},ae={class:"text-2xl font-bold pt-4 pb-3 text-center text-white"},ie={class:"w-[94vw] mx-auto"},le={class:"mb-2"},ce=a("h2",{class:"text-white font-bold text-xl my-3"},"Inference API",-1),de={class:"grid grid-rows-[repeat(2,auto)] gap-y-3 bg-[#4a4a4a] rounded-lg p-4"},ue={ref:"textInference",class:"border border-white/5 bg-[#5b5b5b] px-3 py-2 min-h-24 rounded-lg text-white"},me={class:"bg-[#4a4a4a] rounded-lg px-4 py-3 mb-2 grid grid-rows-3 gap-y-1"},fe={class:"text-white"};function ge(e,t,n,c,r,i){const o=R("CountTo");return g(),p(E,null,[a("h1",ae,_(r.model.modelGroup),1),a("section",ie,[a("div",le,[ce,a("div",de,[a("textarea",ue,null,512),a("button",{onClick:t[0]||(t[0]=(...s)=>i.modelInference&&i.modelInference(...s)),class:"bg-[#1387f8] rounded-lg h-10 text-white"}," Compute ")])]),G(a("div",me,[(g(!0),p(E,null,v(r.model.output,(s,d)=>(g(),p("div",{key:s.label,class:"w-full grid grid-cols-2 justify-between col-span-2"},[a("div",fe,_(s.label),1),j(o,{"start-val":0,"end-val":s.score,duration:1e3,decimals:3,class:"text-right text-white"},null,8,["end-val"])]))),128))],512),[[V,r.model.output]])])],64)}const Me=M(oe,[["render",ge]]),he={props:{processes:{type:Object,required:!1}},components:{ScrollReveal:U}},pe={class:"mx-auto w-[94vw]"},we=a("h2",{class:"text-white font-bold text-xl my-3"},"Production Process",-1),_e={class:"grid grid-rows-2 place-items-center w-10 h-10 mr-5"},ye=a("div",{class:"text-lg text-white"},"STEP",-1),xe={class:"text-lg text-white"},be={class:"flex-grow md:grid md:grid-cols-2 md:gap-x-5"},Ee={class:"text-white font-bold text-lg pb-3"},ke={class:"text-[#d0d0d0]"},Ce={class:"grid grid-rows-[repeat(auto-fill,1fr)] mt-3 gap-y-2"},Se=["href"],Pe={class:"overflow-hidden whitespace-nowrap text-ellipsis"};function ve(e,t,n,c,r,i){const o=R("ScrollReveal");return g(),p("section",pe,[we,(g(!0),p(E,null,v(n.processes,(s,d)=>(g(),H(o,{key:s.id,class:"bg-[#4a4a4a] rounded-lg flex mb-2 p-4"},{default:W(()=>[a("div",_e,[ye,a("div",xe,_((d+1).toString().padStart(2,"0")),1)]),a("div",be,[a("div",null,[a("div",Ee,_(s.title),1),a("div",ke,_(s.text),1)]),a("div",Ce,[(g(!0),p(E,null,v(s.sources,l=>(g(),p("a",{key:l.id,href:l.url,target:"_blank",rel:"noopener noreferrer",class:"border border-solid border-white text-[#d0d0d0] text-sm rounded-lg px-4 h-9 grid items-center"},[a("span",Pe,_(l.name),1)],8,Se))),128))])])]),_:2},1024))),128))])}const Re=M(he,[["render",ve]]);export{Me as M,Re as P};
