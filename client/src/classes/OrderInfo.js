import Order from './Order.js';
export default class OrderInfo extends Order {
    constructor(args) {
        super(args);
        if(args instanceof Object){
            this.photos = JSON.parse(args['photo']);
        }
    }

    addPhotos(array) {
        for (let each of array) {
            this.photos.push(each);
        }
    }
}