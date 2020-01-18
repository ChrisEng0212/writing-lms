
let unit_number = document.getElementById('unit').innerHTML
console.log(unit_number)


$.ajax({    
    type : 'POST',
    url : '/jCheck/work/' + unit_number
   
})
.done(function(data) {            
    if (data.work != 'None') {  
        let whole_obj = JSON.parse(data.work)
        //let meta = whole_obj['meta']
        let plan = whole_obj['plan'] 
        let sources = JSON.parse(data.sources)
        let slides = sources[unit_number]['Materials']                
        //console.log('META: ', meta)
        console.log('PLAN: ', plan)
        console.log('SLIDES: ', slides)
        startVue(plan, slides)
    }
    else{
        console.log('No data')
        let plan = {
            "Topic" : "",
            "Thesis": "", 
            "Idea_1": "", 
            "Details_1": "", 
            "Idea_2": "", 
            "Details_2": "", 
            "Idea_3": "", 
            "Details_3": "", 
        }
        let sources = JSON.parse(data.sources)
        let slides = sources[unit_number]['Materials'] 
        console.log('PLAN: ', plan)
        console.log('SLIDES: ', slides)       
        startVue(plan, slides)
    }
});


function sendData(plan, stage){
    console.log(plan, stage)
    $.ajax({    
        type : 'POST',
        data : {
            unit : document.getElementById('unit').innerHTML, 
            obj : JSON.stringify(plan),
            stage : stage,
            date : 'plan', 
            work : 'plan'           
        },
        url : '/sendData',    
    })
    .done(function(data) {              
        if (data) {                
            alert('Thank you ' + data.name + ', your ' + data.work + ' has been saved')
            window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number         
        }
    });
}


function startVue(plan, slides){ new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'], 
    mounted: function(){        
        this.deSelect('Topic', '0')
        this.deSelect('Thesis', '1') 
        this.deSelect('Idea_1', '2') 
        this.deSelect('Details_1', '3') 
        this.deSelect('Idea_2', '4') 
        this.deSelect('Details_2', '5')
        this.deSelect('Idea_3', '6') 
        this.deSelect('Details_3', '7')        
    }, 
    data: {        
        planOBJ : plan,       
        slides : slides,  
        save : false,        
        control : {}
    }, 

    methods: {
        selectText: function(id){
            console.log(id)  
            document.getElementById(id).setAttribute('class', 'input2')          
        },
        deSelect: function(id, idx){            
            //When ref is used together with v-for, the ref you get will be an array containing the child components mirroring the data source. THEREFORE ADD [0]
            //When using a variable with Refs use '[variable]' instead of .RefNAME
            console.log(this.planOBJ)            
            let string = (this.$refs[id])[0].value
            // but this should be done automatically with v-model???????????????????????????
            
            //check if change has been made before updating object
            if (string != this.planOBJ[id]){
                this.save = true
                this.planOBJ[id] = string                
            } 

            // set class of text box
            if (string.length > 0 ) { 
                let textBox = document.getElementById(id)
                console.log('Height', textBox.scrollHeight)
                textBox.setAttribute('class', 'input3') 
                textBox.setAttribute('style', 'height:' + textBox.scrollHeight +'px !important')
            }
            else { 
                document.getElementById(id).setAttribute('class', 'input1') 
            }                       
                        
            if ( id.indexOf('Det') == 0 ) {
                var ideasList = string.split(',')
                console.log('DETAILS ' + ideasList, typeof(ideasList))
                if (ideasList.length > 1 ){
                    //alert ('You have listed ' + (ideasList.length) + ' details' )
                    document.getElementById(id).setAttribute('class', 'input3')
                    console.log(idx, typeof(idx))
                    this.control[idx] = ideasList.length 
                    console.log(this.control)
                }
                else {
                    //alert ('WARNING: no details found. Please use " , " to seperate you details')
                    document.getElementById(id).setAttribute('class', 'input1')                    
                    console.log(idx, typeof(idx))
                    this.control[idx] = 'None'
                    console.log(this.control)
                }
            }
        },
        readRefs: function(){
            var stage = 1
            console.log(this.planOBJ)
            for(var key in this.planOBJ) {
                if ( key.indexOf('Det') == 0 ) {
                    var detailsValue = this.planOBJ[key]
                    if (Array.isArray(detailsValue)) {
                        console.log('ARRAY ' + detailsValue)
                    }
                    // check details sections     
                    // Lorum , Ipsum  
                    else if (detailsValue.split(',').length <=1 ){
                        alert ('Please make sure you use commas " , " to seperate your details' )   
                        return false                       
                    }
                    else{
                        //replace details with [listed ideas]
                        detailsList = detailsValue.split(',')
                        console.log('UPDATE' + detailsList)
                    } 
                                
                }
                else if (this.planOBJ[key] == ''){
                    alert('Warning! ' + key + ' is not complete yet, please comeback to finish it soon' )  
                    stage = 0                 
                }  
            }            
            sendData(this.planOBJ, stage)
            alert('Please wait a moment while your writing is updating')    
        }, 
        cancel: function(){
            alert('You have cancelled so your changes will not be saved')
            window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number         
        },
        backTo: function(){
            alert('No changes will be saved')
            window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number         
        }        
    }
    
})// end NEW VUE

}// end start vue function