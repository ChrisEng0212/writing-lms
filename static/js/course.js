
$.ajax({    
    type : 'POST',
    url : '/courseCheck',    
})
.done(function(data) { 
         
    if (data) {                
        course = JSON.parse(data.course)
        console.log(course)  
        color =  JSON.parse(data.color)
        startVue(course, color)
    }
});


function startVue(course, color){ new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],  
    data: { 
        course: course,         
    }, 
    methods: {
        style: function(name){
            let styles = {
                G1 : { fontSize : '15px'},
                G2 : { fontSize : '15px'},
                Unit : { fontSize : '30px', fontWeight: 'bold'}, 
                Title : { color : color['titleColor'], fontSize : '20px' }
            }
            return styles[name]
        }
    }    
})


}//end startVue