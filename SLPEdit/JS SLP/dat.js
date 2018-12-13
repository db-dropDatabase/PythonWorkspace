const fs = require('fs');
const data = fs.readFileSync("./empires2_x1_p1.dat");
const Dat = require("genie-dat");
Dat.load(data, (err, data) => {
    fs.writeFileSync("./archer.json", JSON.stringify([].concat.apply([], data.civilizations.map(c => c.objects.filter((i) => i.name === "ARCHR\u0000"))), null, 1))
})