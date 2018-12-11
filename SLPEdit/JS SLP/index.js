let fs = require('fs')
 
// Load a Palette file using the `jascpal` module
let Palette = require('jascpal')
let mainPalette = Palette(fs.readFileSync('50500.bina'))
 
// Load an SLP file and render a frame
let SLP = require('genie-slp')
let slp = SLP(fs.readFileSync('../out.slp'))
let frame = slp.renderFrame(12, mainPalette, { player: 7, drawOutline: true })
 
// Render the returned ImageData object to a PNG file
let { PNG } = require('pngjs')
let png = new PNG({
  width: frame.width,
  height: frame.height
})
png.data = Buffer.from(frame.data.buffer)
png.pack().pipe(fs.createWriteStream('my-file.png'))