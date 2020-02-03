
let unit_number = document.getElementById('unit').innerHTML
console.log(unit_number)

let srcString = document.getElementById('sources').innerHTML
let sources = JSON.parse(srcString)
let slides = sources[unit_number]['Materials']

let fullString = document.getElementById('fullDict').innerHTML
let fullOBJ = JSON.parse(fullString)
let info = JSON.parse(fullOBJ['info']) 
let plan = JSON.parse(fullOBJ['plan']) 
let draft = JSON.parse(fullOBJ['draft']) 

let newPlan = ''
if (plan == null){
    console.log('No data')
    alert('You must complete your plan before you can start the writing')
    window.location = (window.location.href).split('work')[0] + 'work/topic' + '/' + unit_number   
}
else{
    newPlan = {
        0 : [plan['Topic'], plan['Thesis']],
        1 : [plan['Idea_1'], plan['Details_1']], 
        2 : [plan['Idea_2'], plan['Details_2']], 
        3 : [plan['Idea_3'], plan['Details_3']],
        4 : ["", ""]
    }
}

if (draft == null){
    draft = {
        "Intro" : "",
        "Part_1": "", 
        "Part_2": "", 
        "Part_3": "", 
        "Closing": "",            
        }
    }

startVue(newPlan, info, draft)


function startVue(newPlan, info, draft){ 
    let app = new Vue({   

    el: '#vue-app',
    delimiters: ['[[', ']]'],  
    mounted: function(){        
        for (var head in draft){
            this.deSelect(head)
        } 
    },
    data: {
        planOBJ : newPlan,
        infoOBJ : info, 
        draftOBJ : draft,          
        save : false,
        status : info['status'],
        theme : { 'color' : info['theme'] },
        control : {
            0 : [], 
            1 : [], 
            2 : [], 
            3 : [], 
            4 : []
            }, 
        btn_control : {
            very : false, 
            also : false, 
            let  : false, 
            'no matter' : false, 
            there : false, 
            commas : false, 
            words : false
        },
        slides : {
            very : "https://docs.google.com/presentation/d/e/2PACX-1vTlkKekrFpLAINvciyYh_KOxRRGSzikZN27pPoqijHQKlQhbKL0DQzlH6uUx5P862Y6i7Gn1qUASWo2/embed", 
            also : "https://docs.google.com/presentation/d/e/2PACX-1vSaRz0wI_qa8iyIujCJjtEC_M_gJZa7Fw0OLLJbW2_QoQ_yOrezSvn-bvid1m-gR6n1baN1UAptFRFZ/embed", 
            let  : "https://docs.google.com/presentation/d/e/2PACX-1vR7E00mYlONL3h6ZfkYkk0Eyiiz9K2xpSfLnTHMKhqLSCgsEI8tS6lPkIVSqxidm1t1-PT9tIvRkddZ/embed", 
            'no matter' : "https://docs.google.com/presentation/d/e/2PACX-1vQtQUX1hrwY1RwYr229bQcvYgMBOMrfat87pGfWEzxDreQjsBpuCf4rSXokvKehDuE7hNGCloqi2yM9/embed", 
            there : "https://docs.google.com/presentation/d/e/2PACX-1vSmrj_CTJ1xQUF3hn-mnVg43kfGDLnQ9cJUyZUkCuduM-HiVmfTHnlPfxonAk5KqAbfX6o5OR5SeuPZ/embed", 
            commas : "https://docs.google.com/presentation/d/e/2PACX-1vSRaq_OKjKXXlm44qAjnedKcOYZiIBdmF_omtzLKU-mj4i-Mjglq8AsZRCME_OTFtEdwDNlKTkMg4m-/embed", 
            words : "https://docs.google.com/presentation/d/e/2PACX-1vR7E00mYlONL3h6ZfkYkk0Eyiiz9K2xpSfLnTHMKhqLSCgsEI8tS6lPkIVSqxidm1t1-PT9tIvRkddZ/embed", 
            although : "", 
            Intro  : "https://docs.google.com/document/d/e/2PACX-1vQr45ud5ZYkAvB6s6AJ-M-X7PlL1WwjpXzQT1-byPFuMVWw2jSWg5Ejc5AnEdf38lKfYNvWnMJE1mJ2/pub?embedded=true", 
            Part_1 : "https://docs.google.com/document/d/e/2PACX-1vQr45ud5ZYkAvB6s6AJ-M-X7PlL1WwjpXzQT1-byPFuMVWw2jSWg5Ejc5AnEdf38lKfYNvWnMJE1mJ2/pub?embedded=true",  
            Part_2 : "https://docs.google.com/document/d/e/2PACX-1vQr45ud5ZYkAvB6s6AJ-M-X7PlL1WwjpXzQT1-byPFuMVWw2jSWg5Ejc5AnEdf38lKfYNvWnMJE1mJ2/pub?embedded=true",  
            Part_3 : "https://docs.google.com/document/d/e/2PACX-1vQr45ud5ZYkAvB6s6AJ-M-X7PlL1WwjpXzQT1-byPFuMVWw2jSWg5Ejc5AnEdf38lKfYNvWnMJE1mJ2/pub?embedded=true",  
            Closing : "https://docs.google.com/document/d/e/2PACX-1vR3N3BjlVCQvrzBH5zXsK64bIlJniW38G40h3ymgSNlCvHKbOFsIRoEBP9zEyrutvxEPGoMhjm8haFX/pub?embedded=true",  
        },
        helper : {
            Intro : false, 
            Part_1 : false, 
            Part_2 : false, 
            Part_3 : false, 
            Closing : false
        }

    }, 
    methods: {
        selectText: function(id){
            console.log(id)            
            document.getElementById(id).setAttribute('class', 'input2')          
        },
        deSelect: function(id, idx){       
            let string = (this.$refs[id])[0].value  
            console.log('STRING', string, 'ID_INPUT', this.draftOBJ[id])
            //check if change has been made before updating object
            if (string != this.draftOBJ[id]){
                this.save = true
                this.draftOBJ[id] = string   
                console.log('SAVE', string, this.draftOBJ );             
            }
                        

            if (string.length > 0 ) { 
                let textBox = document.getElementById(id)
                console.log('Height', textBox.scrollHeight)
                textBox.setAttribute('class', 'input3') 
                textBox.setAttribute('style', 'height:' + textBox.scrollHeight +'px !important')
            }

            else { 
                document.getElementById(id).setAttribute('class', 'input1') 
            }  

            /// text checking and feedback
            this.control[idx] = []


            if (
                string.indexOf('very like') >= 0 || 
                string.indexOf('very appreciate') >= 0 ||
                string.indexOf('very hate') >= 0 ||
                string.indexOf('very enjoy') >= 0 ||
                string.indexOf('very love') >= 0 
                ){      
                this.control[idx].push('very')
            }           
            
            // take all white space from text            
            console.log(string.replace(/\s\s/g, " "));
            new_string = string.replace(/\s\s/g, " ")

            var feedback = [
                ['very' ,  /very like/i],
                ['very' ,  /very enjoy/i],
                ['very' ,  /very love/i],
                ['very' ,  /very hate/i],
                ['very' ,  /very appreciate/i], 

                ['there' ,  /there have/i],
                ['there' ,  /there has/i],
                ['there' ,  /there had/i],

                ['also' ,  /also can/i],
                ['also' ,  /also is/i],
                ['also' ,  /also will/i],
                ['also' ,  /also am/i],
                ['also' ,  /also are/i], 

                ['no matter' ,  /no matter/i],
                ['let' ,  /let/i],                              
            ]
            
            for (var fb in feedback) {
                if (new_string.match(feedback[fb][1])){
                    this.control[idx].push(feedback[fb][0])
                }                      
            }    
            
            var commaCheck = string.split(',')
            var commas = commaCheck.length
            var periodCheck = string.split('.')
            var periods = periodCheck.length
            if (commas > periods * 1.8 ) {      
                this.control[idx].push('commas')
            }  
            
            var wordCheck = string.split(' ')
            var words = wordCheck.length
            if (string.indexOf('Part') >= 0 && words < 20) {
                this.control[idx].push('word_count')
            }

            console.log(this.control)
        },
        controller: function(item){
            for (btn in this.btn_control){
                if (btn == item){
                   this.btn_control[item] = !this.btn_control[item]  
                }
                else {
                    this.btn_control[btn] = false
                }                
            }           
            console.log(this.btn_control[item])
        },
        helpButton: function(key){
            for (help in this.helper){
                if (help == key){
                   this.helper[help] = !this.helper[help]
                   console.log(help, 'DONE'); 
                }
                else {
                    this.helper[help] = false
                    console.log(help, 'ALSO');
                }                
            }           
            console.log(key, this.helper)
        },
        readRefs: function(){ 
            var count = 0            
            for(var key in this.draftOBJ) {
                if (this.draftOBJ[key] == ''){
                    alert('Warning! ' + key + ' is not complete yet - but you can fix it later' ) 
                    status = 1  
                    date = 'none'                
                } 
                else{
                    count += (this.draftOBJ[key].split(' ')).length
                    if (status = 1) {
                        status = 2
                        //this will catch the first date of completed work
                        date = 'update'
                    }
                    else {
                        status = 2
                        date = 'redo'
                    }
                    
                    console.log('COUNT', count)
                } 
            }
            this.sendData(this.draftOBJ, status) 
            alert('Please wait a moment while your writing is being updated') 
        }, 
        sendData: function (obj, stage){
            console.log(obj, stage)
            $.ajax({    
                type : 'POST',
                data : {
                    unit : document.getElementById('unit').innerHTML, 
                    obj : JSON.stringify(obj),
                    stage : stage,                     
                    work : 'draft'           
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