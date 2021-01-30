// document.getElementById("btnPredict").addEventListener("click", myFunction);

var predictForm=document.getElementById("predictForm")

function handleForm(event) { 
    apiCallFunction()
    event.preventDefault(); 
} 
predictForm.addEventListener('submit', handleForm);

function apiCallFunction() {
var urlPath = document.getElementById("urlForImage").value
document.getElementById("predictImageCategory").style.visibility ="hidden"
console.log(" url of image is ",urlPath)
let data = {"url": urlPath}
document.getElementById("predictProgress").style.visibility="visible"
document.getElementById("predictImageCategoryText").innerText=""
resultTextArea.innerHTML = JSON.stringify("",null,4)

$.ajax( {
    url:"/predict",
  type: "POST", 
  data: JSON.stringify(data),
  contentType: "application/json; charset=UTF-8",
  success: function(result) {
         setResults(result)
    }
})

// this below code is not work
// fetch("/predict", {
//     method: "POST", 
//     request: JSON.stringify(data)
//   }).then(res => {
//     console.log("Request complete! response:", res);
//     setResults(res)
//   });

//  alert("predict clicked");
}

function setResults(predResult){
    console.log(predResult);
    var resultTextArea =document.getElementById("resultTextArea");
    // document.getElementById("resultTextArea").style.visibility="visible";
    resultTextArea.innerHTML = JSON.stringify(predResult,null,4)
    var predictImageCategory =document.getElementById("predictImageCategory")
    predictImageCategory.style.visibility ="visible"
    document.getElementById("predictProgress").style.visibility="hidden"
    var resJsonObject =JSON.parse(JSON.stringify(predResult["result"]))
    console.log(" we have crick : ",resJsonObject["Cricket"]," and baseball : ",resJsonObject["Baseball"])
    if (resJsonObject["Cricket"]>resJsonObject["Baseball"]){
        predictImageCategory.src ="./static/cricket.svg"
        document.getElementById("predictImageCategoryText").innerText="Cricket"
    }else{
        document.getElementById("predictImageCategoryText").innerText="Baseball"
        predictImageCategory.src ="./static/baseball.svg"
    }

}