
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



function sendImage(form_data){
    
    
   
    $.ajax({    
        type : 'POST',
        data : {
            form_data : form_data,            
            unit : unit_number, 
            processData: false,
            contentType: false,
            cache : false,
            dataType : 'json'                 
        },
        url : '/sendImage'   
    })
    .done(function(data) {              
        if (data) {                
            alert(data.image)           
        }
    });    
}

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
    data: {
        publish : revised,       
        meta : meta, 
        title : 'Title',        
        save : false,
        imageSRC : null,        
        theme : { color : meta['theme'],  display:'inline-block', 'font-size': '25px'}    
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
        image: function () {
            selectedFile = document.getElementById('pic').files[0]

            console.log(selectedFile)
            var form_data = new FormData();

            form_data.append('image', document.getElementById('pic').files[0])
            form_data.append()
            console.log(form_data);
            sendImage(form_data)




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