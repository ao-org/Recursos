const fs = require("fs");
const readIni = require("read-ini-file");
const images = require("images");
const jimp = require("jimp");

const ceilPowerOf2 = (x) => Math.pow(2, Math.ceil(Math.log(x) / Math.log(2)));

async function main() {
  const heads = readIni.sync("../init/cabezas.ini");
  const graphics = readIni.sync("../init/graficos.ini");

  const numHeads = +heads["INIT"]["NumHeads"];

  const headSize = 16;
  const outputImageSize = ceilPowerOf2(Math.sqrt(numHeads * headSize * headSize));

  let x = 0,
    y = 0;

  const headsInfo = [];

  const outputImage = images(outputImageSize, outputImageSize);

  let allHeights = [];
  for (let headIndex = 1; headIndex <= numHeads; ++headIndex) {
    const grhIndex = parseInt(heads["HEAD" + headIndex]["Head3"]);
    const grhLine = graphics["Graphics"]["Grh" + grhIndex];

    try {
      const [, fileNum, origX, origY, widthStr, heightStr] = grhLine.split("-");

      let width = parseInt(widthStr);
      let height = parseInt(heightStr);

      const inputImage = images(`../Graficos/${fileNum}.png`);

      const headImage = images(inputImage, parseInt(origX), parseInt(origY), width, height);
      const headImageBuffer = headImage.encode("png");

      const trimmedHeadImage = (await jimp.read(headImageBuffer)).autocrop();
      width = trimmedHeadImage.getWidth();
      height = trimmedHeadImage.getHeight();
      allHeights.push(height);

      const trimmedHeadImageBuffer = await trimmedHeadImage.getBufferAsync(jimp.MIME_PNG);

      if (x + width > outputImageSize) {
        const maxHeight = Math.max(...allHeights);
        x = 0;
        y += maxHeight;
        allHeights = [];
      }

      outputImage.draw(images(trimmedHeadImageBuffer), x, y);

      headsInfo.push({
        id: headIndex,
        x,
        y,
        width,
        height,
      });

      x += width;
    } catch (err) {
      //   if (err.message) console.error(err);
      console.error(`No existe el head ${headIndex}. Salteando index.`);
    }
  }

  outputImage.save("output.png");

  fs.writeFileSync("coords.json", JSON.stringify(headsInfo, null, 4));

  console.log("Creado output.png y coords.json");
}

main();
