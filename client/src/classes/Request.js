class Request{
    uuid = undefined;
    name = undefined;
    msg = undefined;
    state = undefined;
    order_id = undefined;
    requestUserName = undefined;
    constructor(args) {
        this.uuid = args.request_id;
        this.name = args.name;
        this.msg = args.msg;
        this.state = args.state;
        this.order_id = args.order_id;
        this.requestUserName = args.requestUserName;
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