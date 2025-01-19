const x =  [{"JSON":{"batchinfo":"MER - 31515902","canabinoids":28,"cbd":3,"classification":"Sativa","delta_9":12,"grams":3.5,"harvest":"06/21/24","producer":"Paddle Creek Cannabis","strain":"Green Arrow","thc-a":5,"type":"Flower"},"img":"paddle_creek_cannabis_flower.jpg","instock":10,"machineId":1,"merchantId_fk":1,"price":"13.25","rowId":517,"spoolId":"2","storeId_fk":1,"uid":"03684246d"}]

for ( let k in x[0] ) {
    const v = x[0][k]
    console.log( ">" + k + "<" , v )
}
