let unit_number = document.getElementById('unit').innerHTML
console.log(unit_number)

$.ajax({    
    type : 'POST',
    url : '/topicCheck/' + unit_number   
})
.done(function(data) { 
         
    if (data) {  
        console.log(data.dataList);   
        console.log(data.sources);           
        let dataList = data.dataList
        let sources = JSON.parse(data.sources)
        console.log(dataList)   

        startVue(dataList, sources)
    }
    else{
        console.log('ERROR OCCURRED');
    }
});


function startVue(dataList, sources){ 
    var app = new Vue({   

    el: '#vue-app',
    mounted: function {

    },
    delimiters: ['[[', ']]'],  
    data: {
        dataList : dataList, 
        slides : sources[unit_number]['Materials'], 
        deadline : sources[unit_number]['Date']                     
    }, 
    methods: {
                  
    }     

    
})// end NEW VUE

}
