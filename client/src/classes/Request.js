class Request{
    uid = undefined;
    name = undefined;
    msg = undefined;
    state = undefined;
    order_id = undefined;
    slave_id = undefined;
    requesterName = undefined;
    constructor(args) {
        this.uid = args['uid'];
        this.name = args['name'];
        this.msg = args['description'];
        this.state = args['request_status'];
        this.order_id = args['task_id'];
        this.requesterName = args['requester_name'];
        this.slave_id = args['requester_id'];
    };
    updateState(state){
        this.state = state;
    };
    updateMsg(msg){
        this.msg = msg;
    };
    updateRequesterName(name){
        this.requesterName = name;
    }
    updateTitle(name){
        this.name = name;
    };

    updateInfo(req){
        this.updateRequesterName(req['requester_name'])
        this.updateMsg(req['description'])
    }

}
export default Request;