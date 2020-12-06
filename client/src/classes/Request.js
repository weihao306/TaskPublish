class Request{
    uid = undefined;
    name = undefined;
    msg = undefined;
    state = undefined;
    task_id =undefined;
    order_id = undefined;
    slave_id = undefined;
    requesterName = undefined;
    constructor(args) {
        this.uid = args['uid'];
        this.name = args['name'];
        this.msg = args['description'];
        this.state = args['request_status'];
        this.order_id = args['task'];
        this.requesterName = args['requesterName'];
        this.slave_id = args['requester'];
    };
    updateState(state){
        this.state = state;
    };
    updateMsg(msg){
        this.msg = msg;
    };
    updateTitle(name){
        this.name = name;
    };
}
export default Request;