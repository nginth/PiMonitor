function rpiCPUMonitor(req, resp){
    ClearBlade.init({request: req});
    var cpus = req.params.body.split(',').map(function(x) {
        return parseFloat(x);
    });
    var collection = ClearBlade.Collection({collectionName:"rpiCPU"});
    var newRow = {
        time: new Date().toISOString(),
        cpu_0: cpus[0],
        cpu_1: cpus[1],
        cpu_2: cpus[2],
        cpu_3: cpus[3]
    }
    collection.create(newRow, function(err, data) {
        if (err) {
            resp.error(data);
        } else {
            resp.success(newRow);
        }
    });
}