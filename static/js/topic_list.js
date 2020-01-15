
$.ajax({    
    type : 'POST',
    url : '/jCheck/sources/0',    
})
.done(function(data) { 
         
    if (data) {                
        topics = JSON.parse(data.sources)         
        console.log(topics)         
        startVue(topics)
    }
});


function startVue(topics){ new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],  
    data: {
        topics: topics                        
    }, 
    methods: {
                  
    }     

    
})// end NEW VUE

}
