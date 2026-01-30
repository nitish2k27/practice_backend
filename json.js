

product={
    name:"surf-excel",
    price:200,
}

console.log(JSON.stringify(product));//json metohos to convert the js into the json syntax
const jsonstring=JSON.stringify(product);
console.log(JSON.parse(jsonstring));//jsonmethod to convert the json data to js

//localstorage are 
//data stored in local variables are temporar 
// wehn thapage is refresed all tha values gets reseted ayutomatically 
//local storage only supports strings
//local storage helps to not happen this 

localStorage.setItem('messsage','hello');//message is aname of string to store value=hello in local storage
localStorage.getItem('message');//message is to get the string named message