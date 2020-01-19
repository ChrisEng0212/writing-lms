
let unit_number = document.getElementById('unit').innerHTML
console.log(unit_number)

$.ajax({    
    type : 'POST',
    url : '/jCheck/work/' + unit_number
   
})
.done(function(data) {            
    if (data.work !='None') {  
        let whole_obj = JSON.parse(data.work)        
        let meta = whole_obj['meta']
        let revised = whole_obj['revise']['revised']
        console.log('META: ', meta)  
        startVue(meta, revised)
    }
    else{
        console.log('No data')
        alert('You must complete your plan before you can start the writing')        
    }
});


function sendData(revised){
    console.log(revised)
    $.ajax({    
        type : 'POST',
        data : {
            unit : document.getElementById('unit').innerHTML,              
            stage : 5,
            html : 'html',             
            student : 'student', 
            text : 'text',
            revised : revised
        },
        url : '/sendRevise',    
    })
    .done(function(data) {              
        if (data) {                
            alert('Thank you ' + data.name + ', your ' + data.work + ' has been saved')
            window.location = (window.location.href).split('work')[0] + 'blog'
        }
    });
}

function startVue(meta, revised){ 
    let app = new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],  
    mounted: function(){        
        this.deSelect('text', 'start')       
    },
    data: {
        publish : revised,       
        metaOBJ : meta,         
        save : false,
        status : meta['status'],
        theme : { 'color' : meta['theme'] }    
    }, 
    methods: {        
        readRefs: function(){             
            sendData(this.revText) 
            alert('Please wait a moment while your writing is being updated') 
        }, 
        cancel: function(){
            alert('You have cancelled so your changes will not be saved')
            window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number         
        }      
    }
    
})// end NEW VUE

}// end start vue function