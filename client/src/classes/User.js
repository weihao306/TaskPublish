class User {
    uid;
    nick_name;
    account;
    password;
    introduction;
    telephone;
    cert_type;
    cert_number;
    // constructor(){
    //     uid = undefined;
    //     nick_name = undefined;
    //     account = undefined;
    //     password = undefined;
    //     introduction = undefined;
    //     cert_type = undefined;
    //     cert_number = undefined;
    // };
    constructor(args) {
        if (args instanceof Object) {
            this.uid = args.uid;
            this.nick_name = args.nick_name?args.nick_name:"";
            this.account = args.account;
            // this.password = args.password?args.password:"";
            this.introduction = args.introduction?args.introduction:"";
            this.telephone = args.telephone;
            this.cert_type = args.cert_type;
            this.cert_number = args.cert_number;
        }
    }
    set_uid(uid) {
        this.uid = uid;
    }
    set_nick_name(nick_name) {
        this.nick_name = nick_name;
    }
    set_account(account) {
        this.account = account;
    }
    set_password(password) {
        this.password = password;
    }
    set_introduction(introduction) {
        this.introduction = introduction;
    }
    set_telephone(telephone) {
        this.telephone = telephone;
    }
    /**
     * obj:{
     *      nick_name,
     *      telephone,
     *      introduction 
     *     }
     */
    updateInfo(obj) {
        this.set_nick_name(obj.nick_name);
        this.set_password(obj.password);
        this.set_telephone(obj.telephone);
        this.set_introduction(obj.introduction);
    }

}
export default User;