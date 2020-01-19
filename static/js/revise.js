
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
        let html = whole_obj['revise']['html']
        let text = whole_obj['revise']['text'] 
        console.log('META: ', meta)  
        startVue(meta, html, text)
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
            stage : 4,
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
            window.location = (window.location.href).split('work')[0] + 'work/publish' + '/' + unit_number   
        }
    });
}

function startVue(meta, revise, text){ 
    let app = new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],  
    mounted: function(){        
        this.deSelect('text', 'start')       
    },
    data: {
        revText : text,
        revHTML : revise,
        metaOBJ : meta,         
        save : false,
        status : meta['status'],
        theme : { 'color' : meta['theme'] }    
    }, 
    methods: {
        selectText: function(id){
            console.log(id)            
            document.getElementById(id).setAttribute('class', 'input2')          
        },
        deSelect: function(id, start){
            if (start!='start') {
                this.save = true
                }    
            
            console.log('SAVE', this.revText );            
              
            let textBox = document.getElementById(id)
            console.log('Height', textBox.scrollHeight)
            textBox.setAttribute('class', 'input3') 
            textBox.setAttribute('style', 'height:' + textBox.scrollHeight +'px !important')
            
        },
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