class OrderInfo {
    uuid = undefined;
    name = undefined;
    info = undefined;
    currentSummoningCount = undefined;
    maximumSummoningCount = undefined;
    status = undefined;
    date = undefined;
    master_uuid = undefined;
    type = undefined;
    photos = [];
    constructor(args) {
        if (args instanceof Object) {
            this.uuid = args['uuid']
            this.name = args['name'];
            this.info = args['info'];
            this.currentSummoningCount = args['currentSummoningCount'];
            this.maximumSummoningCount = args['maximumSummoningCount'];
            this.status = args['status'];
            this.date = args['date'];
            this.master_uuid = args['master_uuid'];
            this.type = args['type'];
            this.photos = args['photos'];
        }
    }
    setPhotos(array){
        this.photos = array;
    }
    addPhotos(array){
        for(let each of array){
            this.photos.push(each);
        }
    }
}
export default OrderInfo;