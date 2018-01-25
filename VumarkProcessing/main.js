var pictoRay = [];
var index = 0;
window.onload = () => {
    document.querySelector("#next").addEventListener("click", () => {
        //get the data
        let pictoThing = [...document.querySelectorAll('.radio')].map((elem) => {
            return [...elem.childNodes].filter((elem) => {
                return elem.checked;
            })[0].value;
        });
        //push back data
        let out = {
            fname: index + '.jpg',
            glare: pictoThing[0],
            light: pictoThing[1],
            print: pictoThing[2],
            type: "right",
            blur: pictoThing[3],
            balls: pictoThing[4]
        };
        if(!pictoRay[index]) pictoRay.push(out);
        else pictoRay[index] = out;
        console.log(out);
        //get the next image
        index++;
        document.querySelector('#img').style.backgroundImage = 'url("right/' + index + '.jpg")';
    });

    document.querySelector('#prev').addEventListener("click", () => {
        index--;
        document.querySelector('#img').style.backgroundImage = 'url("right/' + index + '.jpg")';
    });

    document.querySelector('#img').style.backgroundImage = 'url("right/' + index + '.jpg")';
};