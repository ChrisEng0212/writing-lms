
let jString = document.getElementById('recs').innerHTML
console.log(jString)
const newOBJ = JSON.parse(jString)
console.log(newOBJ)


 
let app = new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],      
    data: {
        recOBJ : newOBJ
    }, 
    methods: {
        goToRevise : function (student, unit){
            window.location = (window.location.href).split('dashboard')[0] + 'editor/' + student + '/' + unit  
        }
        
    }
    
})// end NEW VUE

