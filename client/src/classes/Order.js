class Order {
    uuid = undefined;
    name = undefined;
    info = undefined;
    currentSummoningCount = undefined;
    maximumSummoningCount = undefined;
    modifyInfo = false;
    deleteInfo = false;
    status = undefined;
    date = undefined;
    type = undefined;
    joinRequests =[{
        massess_uuid:undefined,
        request_msg:undefined
    }];
    time = {
        hour:Number,
        minute:Number
    };
    // uuid,name, info, currentSummoningCount, maximumSummoningCount
    constructor(args) {
        this.uuid = args["uuid"];
        this.name = args["name"];
        this.info = args["info"];
        this.currentSummoningCount = args["currentSummoningCount"];
        this.maximumSummoningCount = args["maximumSummoningCount"];
        this.type = args['type'];
        this.status = args["status"];
        this.date = args["date"];
        this.joinRequests = args["joinRequest"]
    }
}
export default Order;