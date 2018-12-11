let fs = require('fs')
 
// Load a Palette file using the `jascpal` module
let Palette = require('jascpal')
let mainPalette = Palette(fs.readFileSync('50500.bina'))
let ret = [];

for(let i = 0, len = mainPalette.length; i < len; i++) {
    ret.push([i < 16 ? "0x0" + i.toString(16) : "0x" + i.toString(16), `#${mainPalette[i].map(i => i < 16 ? "0" + i.toString(16) : i.toString(16)).join("")}`]);
}

let Parse = require("papaparse");

fs.writeFileSync("pal.csv", Parse.unparse({
    fields: ["index", "color"],
    data: ret,
}));