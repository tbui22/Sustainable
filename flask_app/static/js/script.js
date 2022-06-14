fetch("https://type.fit/api/quotes")
    .then(response => response.json() )
    .then(data => console.log(data) )
    .catch(err => console.log(err) )
    
async function getapi() {
    // var quoteDiv= document.querySelector('#quote');
    var response = await fetch("https://type.fit/api/quotes");
    var data = await response.json();
    // console.log(data);
    // var quote = data[Math.floor(Math.random() * data.length)].text;
    appendData(data)
    return data;
    }


function appendData(data){
    console.log(data);
    var quoteText= document.getElementById("quote");
    var authorText= document.getElementById("author");
    var index=Math.floor(Math.random() * data.length)
    quoteText.innerHTML = ' " ' + data[index].text + ' " ';
    authorText.innerHTML = "-" + data[index].author;
}
