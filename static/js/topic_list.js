
$.ajax({    
    type : 'POST',
    url : '/topicCheck',    
})
.done(function(data) { 
         
    if (data) {                
        topics = JSON.parse(data.topics)
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
