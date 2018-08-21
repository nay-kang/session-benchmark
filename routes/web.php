<?php

use Illuminate\Support\Facades\Redis;
use Illuminate\Support\Facades\DB;

/*
 |--------------------------------------------------------------------------
 | Application Routes
 |--------------------------------------------------------------------------
 |
 | Here is where you can register all of the routes for an application.
 | It is a breeze. Simply tell Lumen the URIs it should respond to
 | and give it the Closure to call when that URI is requested.
 |
 */

$router->get('/', function () use ($router) {
    //just for benchmark the framework
    return 'hello world';
    //return $router->app->version();
});

//Simulate new client Token
$token = uniqid();

// Fake Token Data for benchmark
$example_data = [
    'created_at' => time(),
    'client' => 'api_client',
    'scope' => ['scope_1','scope_2','scope_3'],
    'refresh_code' => 'QWERTYUIOPASDFGHJKLZXCVBNMQWERTYUIOPASDFGHJKLZXCVBNM'
];

//how long will session/token expire
const SESSION_LIFETIME = 3600;
function get_session_expired_at(){
    $d = new DateTime();
    $d->setTimestamp(time()+SESSION_LIFETIME);
    return $d;
}

/**
 * there steps
 * 1,insert new session
 * 2,get inserted session
 * 3,update expire time
 */

//redis session
$router->get('/redis',function() use ($token,$example_data){
    $redis = Redis::connection('default');
    
    //insert new session
    $redis->setex($token,SESSION_LIFETIME,json_encode($example_data));
    
    //find session
    $r = $redis->get($token);
    
    //update expire time
    $redis->setex($token,SESSION_LIFETIME,json_encode($example_data));
    return "";
});

//mongodb session
$router->get('/mongodb',function() use ($token,$example_data){

    //advantage for mongodb,there is no need for json encode
    //$data = json_encode($example_data);
    
    //insert new Session
    $data = $example_data;
    $expiredAt = get_session_expired_at();
    $expiredAt = $expiredAt->getTimestamp();
    $collection = (new MongoDB\Client(config('database.connections.mongodb.uri')))->session->session;
    $r = $collection->insertOne(['_id' => $token, 'data' => $data,'expired_at'=>$expiredAt]);
    
    //find session
    $r = $collection->findOne(['_id'=>$token]);
    
    //update expire time
    $expiredAt = get_session_expired_at();
    $expiredAt = $expiredAt->getTimestamp();
    $r = $collection->updateOne(
        ['_id'=>$token],
        ['$set'=>['data'=>$data,'expired_at'=>$expiredAt]]);
});

/*
create table session(
    token char(32) primary key,
    data varchar(2048) null,
    expired_at timestamp null
)
 */
$router->get('/mysql',function() use ($token,$example_data){
    $data = json_encode($example_data);
    
    //insert new session
    $expiredAt = get_session_expired_at();
    $r = DB::insert('insert into session values(?,?,?)',[$token,$data,$expiredAt,$data,$expiredAt]);
    
    //find session
    $r = DB::select('select * from session where token=?',[$token])[0];
    
    //update expire time
    $expiredAt = get_session_expired_at();
    $r = DB::update('update session set data=?,expired_at=? where token=?',[$data,$expiredAt,$token]);
});
                