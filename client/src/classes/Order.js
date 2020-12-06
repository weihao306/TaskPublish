class Order {
    uid = undefined;
    master_id = undefined;
    name = undefined;
    info = undefined;
    currentSummoningCount = undefined;
    maximumSummoningCount = undefined;
    modifyInfo = false;
    deleteInfo = false;
    status = undefined;
    start_date = undefined;
    end_date = undefined;
    type = undefined;
    photos =undefined;
    joinRequests =[{
        massess_uid:undefined,
        request_msg:undefined
    }];
    time = {
        hour:Number,
        minute:Number
    };
    // uid,name, info, currentSummoningCount, maximumSummoningCount
    constructor(args) {
        this.uid = args["uid"];
        this.master_id = args["master"]
        this.name = args["task_name"];
        this.info = args["description"];
        this.currentSummoningCount = args["cur_people"];
        this.maximumSummoningCount = args["max_people"];
        this.type = args['task_type'];
        this.status = args["task_status"];
        this.end_date = args["end_time"];
        this.joinRequests = args["joinRequest"];
    }

    getPhotos(args){
        this.photos = args["photos"];
    }
}
export default Order;