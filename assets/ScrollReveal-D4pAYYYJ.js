import{_ as c,o as d,c as p,t as m,j as V,n as y}from"./index-C28b1HbE.js";let o=0;const u="webkit moz ms o".split(" ");let r,n;const b=typeof window>"u";if(b)r=function(){},n=function(){};else{r=window.requestAnimationFrame,n=window.cancelAnimationFrame;let t;for(let e=0;e<u.length&&!(r&&n);e++)t=u[e],r=r||window[t+"RequestAnimationFrame"],n=n||window[t+"CancelAnimationFrame"]||window[t+"CancelRequestAnimationFrame"];(!r||!n)&&(r=function(e){const i=new Date().getTime(),a=Math.max(0,16-(i-o)),s=window.setTimeout(()=>{e(i+a)},a);return o=i+a,s},n=function(e){window.clearTimeout(e)})}const w={props:{startVal:{type:Number,required:!1,default:0},endVal:{type:Number,required:!1,default:2017},duration:{type:Number,required:!1,default:3e3},autoplay:{type:Boolean,required:!1,default:!0},decimals:{type:Number,required:!1,default:0,validator(t){return t>=0}},decimal:{type:String,required:!1,default:"."},separator:{type:String,required:!1,default:","},prefix:{type:String,required:!1,default:""},suffix:{type:String,required:!1,default:""},useEasing:{type:Boolean,required:!1,default:!0},easingFn:{type:Function,default(t,e,i,a){return i*(-Math.pow(2,-10*t/a)+1)*1024/1023+e}}},data(){return{localStartVal:this.startVal,displayValue:this.formatNumber(this.startVal),printVal:null,paused:!1,localDuration:this.duration,startTime:null,timestamp:null,remaining:null,rAF:null}},computed:{countDown(){return this.startVal>this.endVal}},watch:{startVal(){this.autoplay&&this.start()},endVal(){this.autoplay&&this.start()}},mounted(){this.autoplay&&this.start(),this.$emit("mountedCallback")},methods:{start(){this.localStartVal=this.startVal,this.startTime=null,this.localDuration=this.duration,this.paused=!1,this.rAF=r(this.count)},pauseResume(){this.paused?(this.resume(),this.paused=!1):(this.pause(),this.paused=!0)},pause(){n(this.rAF)},resume(){this.startTime=null,this.localDuration=+this.remaining,this.localStartVal=+this.printVal,r(this.count)},reset(){this.startTime=null,n(this.rAF),this.displayValue=this.formatNumber(this.startVal)},count(t){this.startTime||(this.startTime=t),this.timestamp=t;const e=t-this.startTime;this.remaining=this.localDuration-e,this.useEasing?this.countDown?this.printVal=this.localStartVal-this.easingFn(e,0,this.localStartVal-this.endVal,this.localDuration):this.printVal=this.easingFn(e,this.localStartVal,this.endVal-this.localStartVal,this.localDuration):this.countDown?this.printVal=this.localStartVal-(this.localStartVal-this.endVal)*(e/this.localDuration):this.printVal=this.localStartVal+(this.endVal-this.localStartVal)*(e/this.localDuration),this.countDown?this.printVal=this.printVal<this.endVal?this.endVal:this.printVal:this.printVal=this.printVal>this.endVal?this.endVal:this.printVal,this.displayValue=this.formatNumber(this.printVal),e<this.localDuration?this.rAF=r(this.count):this.$emit("callback")},isNumber(t){return!isNaN(parseFloat(t))},formatNumber(t){t=t.toFixed(this.decimals),t+="";const e=t.split(".");let i=e[0];const a=e.length>1?this.decimal+e[1]:"",s=/(\d+)(\d{3})/;if(this.separator&&!this.isNumber(this.separator))for(;s.test(i);)i=i.replace(s,"$1"+this.separator+"$2");return this.prefix+i+a+this.suffix}},destroyed(){n(this.rAF)}};function g(t,e,i,a,s,f){return d(),p("span",null,m(s.displayValue),1)}const l=c(w,[["render",g]]);function S(t,e,i){return e in t?Object.defineProperty(t,e,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[e]=i,t}function h(t,e){var i=Object.keys(t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(t);e&&(a=a.filter(function(s){return Object.getOwnPropertyDescriptor(t,s).enumerable})),i.push.apply(i,a)}return i}l.unmounted=l.destroyed,Reflect.deleteProperty(l,"destroyed");var _=function(t){for(var e=1;e<arguments.length;e++){var i=arguments[e]!=null?arguments[e]:{};e%2?h(Object(i),!0).forEach(function(a){S(t,a,i[a])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(i)):h(Object(i)).forEach(function(a){Object.defineProperty(t,a,Object.getOwnPropertyDescriptor(i,a))})}return t}({name:"CountTo",emits:["callback","mountedCallback"]},l);const D={data(){return{isVisible:!1}},mounted(){const t=new IntersectionObserver(e=>{e.forEach(i=>{i.isIntersecting&&(this.isVisible=!0,t.unobserve(this.$refs.revealElement))})});t.observe(this.$refs.revealElement)}};function F(t,e,i,a,s,f){return d(),p("div",{ref:"revealElement",class:y(["opacity-0",{"animate__animated animate__fadeIn":s.isVisible}])},[V(t.$slots,"default")],2)}const v=c(D,[["render",F]]);export{_ as C,v as S};
