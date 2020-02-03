
let unit_number = document.getElementById('unit').innerHTML
console.log(unit_number)

let fullString = document.getElementById('fullDict').innerHTML
let fullOBJ = JSON.parse(fullString)
console.log(fullOBJ);
let info = JSON.parse(fullOBJ['info']) 
let revise = JSON.parse(fullOBJ['revise']) 
console.log(revise);
let html = revise['html']
let text = revise['text'] 

if (revise == null){
    console.log('No data')
    alert('Please wait for instructors revision')
    window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number   
}

startVue(info, html, text)


function startVue(info, html, text){ 
    let app = new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],  
    mounted: function(){        
        this.deSelect('text', 'start')       
    },
    data: {
        original : text,
        revText : text, // updated by v-model
        revHTML : html,
        infoOBJ : info,         
        save : false,
        status : info['status'],
        theme : { 'color' : info['theme'] }    
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
            this.sendData(this.revText) // revText connected by v-model
            alert('Please wait a moment while your writing is being updated') 
        }, 
        sendData: function (revised){
            console.log(revised)
            $.ajax({    
                type : 'POST',
                data : {
                    unit : document.getElementById('unit').innerHTML, 
                    obj : revised,
                    stage : 4,                     
                    work : 'revise'           
                },
                url : '/storeData',    
            })
            .done(function(data) {              
                if (data) {                
                    alert('Thank you ' + data.name + ', your ' + data.work + ' has been saved')
                    window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number         
                }
            });
        },
        cancel: function(){
            alert('You have cancelled so your changes will not be saved')
            window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number         
        }      
    }
    
})// end NEW VUE

}// end start vue function