import Order from './Order.js';
export default class OrderInfo extends Order {
    constructor(args) {
        super(args);

    }

    addPhotos(array) {
        for (let each of array) {
            this.photos.push(each);
        }
    }
}