let unit_number = document.getElementById('unit').innerHTML
console.log(unit_number)

$.ajax({    
    type : 'POST',
    url : '/topicCheck/' + unit_number   
})
.done(function(data) { 
         
    if (data) {         
        let dataList = data.dataList // this is a list so cannot Jparse
        let sources = JSON.parse(data.sources)
        let stage = data.stage
        console.log(dataList, typeof(dataList)) 
        console.log(stage, typeof(stage));  

        startVue(dataList, sources, stage)
    }
    else{
        console.log('ERROR OCCURRED');
    }
});


function startVue(dataList, sources, stage){ 
    var app = new Vue({   

    el: '#vue-app',
    mounted: function(){
        this.loadData(dataList)
        this.setStage(parseInt(stage))           
    },
    delimiters: ['[[', ']]'],  
    data: {
        dataList : dataList, 
        slides : sources[unit_number]['Materials'], 
        deadline : sources[unit_number]['Deadline'], 
        stage : stage, 
        pubs : [], 
        drafts : [], 
        plans : [],   
        buttons : {
            plan : true, 
            draft : false, 
            revise : false, 
            publish : false
        }

                      
    }, 
    methods: {
        loadData: function(dataList){
            for (obj in dataList) {
                var work =  JSON.parse(dataList[obj])
                console.log('WORK', work)
                //cascading conditionals to fill up the lists   
                if (work['info']['stage'] > 2) {
                    if (this.pubs.length < 2 ) {                        
                        this.pubs.push(work)
                        console.log('PUBLISH_LENGTH', this.plans.length)
                        continue
                    }                                        
                }
                if (work['info']['stage'] > 1) {
                    if (this.drafts.length < 2 ) {
                        this.drafts.push(work)
                        console.log('PLAN_LENGTH', this.drafts.length)
                        console.log(this.draft);
                        continue
                    }                    
                }
                if (work['info']['stage'] > 0){
                    if (this.plans.length < 2 ) {
                        console.log('DRAFTS_LENGTH', this.plans.length)
                        console.log(this.plans);
                        this.plans.push(work)
                        continue
                     }                       
                }  
                
                
                console.log('Not added ', work);             
                
            }// end for

        }, 
        color: function(theme){
            return  { color: theme }
        },
        goTo: function(work){           
            window.location = (window.location.href).split('work')[0] + 'work/' + work + '/' + unit_number
        },
    
        setStage: function(stage){            
            if (stage > 0) {               
                this.buttons['draft'] = true
            } 
            if (stage > 2) {
                this.buttons['revise'] = true
            } 
            if (stage > 3) {
                this.buttons['publish'] = true
            }

        }
                  
    }     

    
})// end NEW VUE

}
