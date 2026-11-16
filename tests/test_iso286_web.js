/* Same dataset and engine shipped in the external static website. */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'..'),ctx={CAD_FIT_DATA:JSON.parse(fs.readFileSync(path.join(root,'references/iso-286-1-2010.json'),'utf8'))};vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(root,'web/iso286.js'),'utf8'),ctx);const e=ctx.CADISO286;
for(const [code,lo,hi] of [['H8/f7',.025,.089],['H7/n6',-.033,.008],['H7/s6',-.059,-.018]])assert.deepStrictEqual(Array.from(e.calculate(code,36).signed_difference_mm),[lo,hi]);
assert.deepStrictEqual(Array.from(e.calculate('H7/g6',20).signed_difference_um),[7,41]);
assert(e.recommend('hole','clearance',20,'0.007','0.041').some(x=>x.designation==='H7/g6'));
assert(!e.recommend('hole','clearance',20,'0.007001','0.041').some(x=>x.designation==='H7/g6'));
assert(!e.recommend('hole','clearance',20,'0.007','0.040999').some(x=>x.designation==='H7/g6'));
for(const n of ['NaN','Infinity',0,501,true,'20.0000001'])assert.throws(()=>e.calculate('H7/g6',n));
assert.throws(()=>e.calculate('H7/jS6',20));assert.throws(()=>e.recommend('hole','clearance',20,'.2','.1'));
for(const basis of ['hole','shaft'])for(const row of ctx.CAD_FIT_DATA.candidates[basis])for(const size of [1,3,6,10,18,20,36,50,65,80,120,180,250,300,400,500]){const r=e.calculate(row.code,size);assert(r.signed_difference_um[0]<=r.signed_difference_um[1]);}
console.log('ISO browser engine regression tests: OK');
