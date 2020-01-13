
let unit_number = document.getElementById('unit').innerHTML
console.log(unit_number)

$.ajax({    
    type : 'POST',
    url : '/jCheck/plan/' + unit_number
   
})
.done(function(data) {            
    if (data.data !='None') {                
        console.log(data.data)
        startVue(JSON.parse(data.data))
    }
    else{
        console.log('No data')
        let inputObj = {
            'Topic' : 'nuts, sacks',
            'Thesis': 'nuts, balls', 
            'Idea-1': 'nuts, balls', 
            'Details-1': 'nuts, balls', 
            'Idea-2': 'nuts, balls', 
            'Details-2': 'nuts, balls', 
            'Idea-3': 'nuts, balls', 
            'Details-3': 'nuts, balls', 
        }
        startVue(inputObj)
    }
});


function sendData(obj){
    console.log(obj)
    $.ajax({    
        type : 'POST',
        data : {
            unit : document.getElementById('unit').innerHTML, 
            obj : JSON.stringify(obj),
            stage : '1'
        },
        url : '/sendData',    
    })
    .done(function(data) {              
        if (data) {                
            alert('Thank you ' + data.name + ', your plan has been saved')
        }
    });
}


function startVue(inputObj){ new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],  
    data: {
        inputObj : inputObj                    
    }, 
    methods: {
        selectText: function(id){
            console.log(id)            
            document.getElementById(id).setAttribute('class', 'input2')          
        },
        deSelect: function(id){
            //When ref is used together with v-for, the ref you get will be an array containing the child components mirroring the data source. THEREFORE ADD [0]
            //When using a variable with Refs use '[variable]' instead of .RefNAME
            console.log(this.inputObj)
            let string = (this.$refs[id])[0].value
            if (string.length > 0 ) { 
                let textBox = document.getElementById(id)
                console.log('Height', textBox.scrollHeight)
                textBox.setAttribute('class', 'input3') 
                textBox.setAttribute('style', 'height:' + textBox.scrollHeight +'px !important')
            }
            else { 
                document.getElementById(id).setAttribute('class', 'input1') 
            }                       
            
            console.log('check ' + id + ' : ' + string)
            console.log(id.indexOf('Det'))
            if ( id.indexOf('Det') == 0 ) {
                var ideasList = string.split(',')
                
                if (ideasList.length > 1 ){
                    //alert ('You have listed ' + (ideasList.length) + ' details' )
                    document.getElementById(id).setAttribute('class', 'input3')
                }
                else {
                    alert ('WARNING: no details found. Please use " , " to seperate you details')
                    document.getElementById(id).setAttribute('class', 'input1')
                }

            }
        },
        readRefs: function(){
            for(var key in inputObj) {
                if ( key.indexOf('Det') == 0 ) {
                    var detailsValue = inputObj[key]
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
                else if (inputObj[key] == ''){
                    alert('Warning! ' + key + ' is not complete yet' )
                    return false
                }  
            }
            
            sendData(inputObj)            
                     
        }       
    }
    
})// end NEW VUE

}// end start vue function