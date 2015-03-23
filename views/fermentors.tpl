<html>
<head>
	<title>Fermentors</title>
	<!-- Bootstrap -->
    <link type="text/css" href="/static/css/bootstrap.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/moment.js"></script>

    <script src= "http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.min.js"></script>

</head>
<body  ng-app="myApp" ng-controller="fermentorController" >

<DIV class="container">

    <TABLE class="table table-striped">
            <THEAD>
                <TH>Inactivate</TH>
                <TH>Edit</TH>
                <TH>Hostname</TH>
                <TH>Name</TH>
                <TH>Fermwrap Pin</TH>
                <TH>Start Date</TH>
                <TH>End Begin Date</TH>
                <TH>End End Date</TH>
                <TH>Start Temp</TH>
                <TH>Temp Differential</TH>
                <TH>Yeast</TH>
                <TH>OG</TH>
                <TH>FG</TH>
                <TH>Material</TH>
                <TH>Probes</TH>
                <TH>Schedule</TH>
            </THEAD>
            <TBODY>

                    <TR ng-repeat="fermentor in fermentors">
                        <TD>
                            <BUTTON class="btn" ng-click="inactivateFermentor(fermentor.id)">
                                 <SPAN class="glyphicon glyphicon-trash"></SPAN>&nbsp;&nbsp;Inactivate
                            </BUTTON>
                        </TD>
                        <TD>
                            <BUTTON class="btn" ng-click="editFermentor(fermentor.id)">
                                <SPAN class="glyphicon glyphicon-pencil"></SPAN>&nbsp;&nbsp;Edit
                            </BUTTON>
                        </TD>
                        <TD><SPAN ng-bind="fermentor.hostname"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.name"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.fermwrap"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.start_date"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.end_begin_date"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.end_end_date"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.start_temp"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.temp_differential"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.yeast"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.og"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.fg"></SPAN></TD>
                        <TD><SPAN ng-bind="fermentor.material"></SPAN></TD>
                        <TD>
                            <TABLE class="table table-striped">
                                <THEAD>
                                    <TH>File Name</TH>
                                    <TH>Type</TH>
                                </THEAD>
                                <TBODY>

                                    <TR ng-repeat="probe in fermentor.probes">
                                        <TD><SPAN ng-bind="probe.file_name"></SPAN></TD>
                                        <TD><SPAN ng-bind="probe.type"></SPAN></TD>
                                    </TR>

                                </TBODY>
                            </TABLE>
                        </TD>
                        <TD>
                            <TABLE class="table table-striped">
                                <THEAD>
                                    <TH>Dt</TH>
                                    <TD>Temp</TD>
                                </THEAD>
                                <TBODY>
                                    <TR ng-repeat="schedule in fermentor.schedules">
                                        <TD><SPAN ng-bind="schedule.dt"></SPAN></TD>
                                        <TD><SPAN ng-bind="schedule.temp"></SPAN></TD>
                                    </TR>
                                </TBODY>
                            </TABLE>
                        </TD>
                    </TR>

        </TBODY>
    </TABLE>


<HR />

<BUTTON class="btn btn-success" ng-click="editFermentor('new')">
    <SPAN class="glyphicon glyphicon-user"></SPAN> Create New Fermentor
</BUTTON>

<HR />

<H3 ng-show="create">Create New Fermentor:</H3>
<H3 ng-show="edit">Edit Fermentor:</H3>



<DIV ng-show="create || edit">
    <FORM name="myForm">
    <TABLE class="table">
        <THEAD>
            <TH>Hostname</TH>
            <TH>Name</TH>
            <TH>Fermwrap Pin</TH>
            <TH>Start Date</TH>
            <TH>End Begin Date</TH>
            <TH>End End Date</TH>
            <TH>Start Temp</TH>
            <TH>Temp Differential</TH>
            <TH>Yeast</TH>
            <TH>OG</TH>
            <TH>FG</TH>
            <TH>Material</TH>
        </THEAD>
        <TBODY>
            <TR>
                <TD>
                    <SELECT ng-model="fermentor.host_id"><OPTION ng-repeat="host in hosts" value="{{'{{host.id}}'}}" >{{'{{host.hostname}}'}}</OPTION></SELECT>
                </TD>
                <TD><INPUT ng-model="fermentor.name" type="text" /></TD>
                <TD>
                    <SELECT ng-model="fermentor.fermwrap"><OPTION ng-repeat="fermwrap in fermwraps" value="{{'{{fermwrap.fermwrap}}'}}">{{'{{fermwrap.fermwrap}}'}}</OPTION></SELECT>
                </TD>
                <TD><INPUT ng-model="fermentor.start_date" type="text" /></TD>
                <TD><INPUT ng-model="fermentor.end_begin_date" type="text"  /></TD>
                <TD><INPUT ng-model="fermentor.end_end_date" type="text"  /></TD>
                <TD><INPUT ng-model="fermentor.start_temp" type="text"  /></TD>
                <TD><INPUT ng-model="fermentor.temp_differential" type="text"  /></TD>
                <TD><INPUT ng-model="fermentor.yeast" type="text" name="yeast" /></TD>
                <TD><INPUT ng-model="fermentor.og" type="text" /></TD>
                <TD><INPUT ng-model="fermentor.fg" type="text" /></TD>
                <TD><INPUT ng_model="fermentor.material" type="text"/></TD>

            </TR>
        </TBODY>
    </TABLE>


    <TABLE class="table table-striped">
        <THEAD>
            <TH>Probe File Name</TH>
            <TH>Probe Type</TH>
        </THEAD>
        <TBODY>
            <TR ng-repeat="probe in fermentor.probes">
                <TD>
                    <SELECT ng-model="probe.file_name" ng-options="probe for probe in probes">



                    </SELECT>
                </TD>
                <TD>
                    <SELECT ng-model="probe.type" ng-options="probe_type for probe_type in probe_types">


                    </SELECT>
                </TD>
            </TR>

        </TBODY>
    </TABLE>
    <BUTTON class="btn" ng-click="add_probe()">Add Probe</BUTTON>
    <BUTTON class="btn" ng-click="remove_probe()">Remove Probe</BUTTON>
    <BR />
    <STRONG>Schedule</STRONG>
    <TABLE id="schedule_table" class="table">
        <THEAD>
            <TH>Date Time</TH>
            <TH>Temp</TH>
        </THEAD>
        <TBODY>
            <TR ng-repeat="schedule in fermentor.schedules">
                <TD>
                    <INPUT ng-model="schedule.dt" />
                </TD>
                <TD>
                    <INPUT ng-model="schedule.temp" />
                </TD>
                <TD>
                    <BUTTON class="btn" ng-click="add_schedule(schedule.index)">Add Schedule</BUTTON>
                    <BUTTON class="btn" ng-click="remove_schedule(schedule.index)">Remove Schedule</BUTTON>
                    <BUTTON class="btn" ng-click="increase_schedule(schedule.index)">Increase Schedule</BUTTON>
                    <BUTTON class="btn" ng-click="decrease_schedule(schedule.index)">Decrease Schedule</BUTTON>
                </TD>
            </TR>

        </TBODY>
    </TABLE>
       <BUTTON class="btn" ng-hide="is_scheduled" ng-click="create_schedule()">Add Schedule</BUTTON>


    <input name="schedule_index" id="schedule_index" type="hidden" />

    </FORM>

<HR />

<BUTTON ng-click="update()" class="btn btn-success">
    <SPAN class="glyphicon glyphicon-save"></SPAN> Save Changes
</BUTTON>
<SPAN ng-show="save_error" class="danger">Save Failed.</SPAN>

</DIV>

</DIV>

<DIV id="inactivateModel" class="modal fade">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal"></button>
                <h4 class="modal-title">Confirmation</h4>
            </div>
            <div class="modal-body">
                <p>Do you really wish to inactivate this fermentor?</p>
                <p class="text-danger"><small>You will not be able to reactivate it.</small></p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Inactivate Fermentor</button>
            </div>
        </div>
    </div>
</DIV>



<script>
    angular.module('myApp', []).controller('fermentorController', ['$scope',  '$http', function($scope, $http) {

        console.log("WTF");

        $scope.inactivateFermentor = function(id) {
            $http.post('/fermentation/fermentor/inactivate', angular.toJson({'id':id}))
            .success(function(data, status, headers, config) {
                // Need a way to iterate over the key, value pairs in index_order (Remember index order is of form {fermentor_id:index} )
                // and decrement each value by one where the value > id
                for (var key in $scope.index_order) {
                    if ($scope.index_order[key] > $scope.index_order[id]) {
                        $scope.index_order[key]--;
                    }
                }

                console.log("slicing");
                console.log("index is " + $scope.index_order[id])
                $scope.fermentors.splice($scope.index_order[id], 1);
                console.log(JSON.stringify($scope.fermentors));

                delete $scope.index_order[id];
            })
            .error(function(data, status, headers, config) {

            });
        }

        $scope.remove_schedule = function(index) {
            //alert("index is " + index + " length is " + $scope.fermentor.schedules.length + "array is " + JSON.stringify($scope.fermentor.schedules));
            console.log("index = " + index);
            console.log("$scope.fermentor.schedules.length = " + $scope.fermentor.schedules.length);
            console.log("$scope.fermentor.schedules = " + angular.toJson($scope.fermentor.schedules));
            if ($scope.fermentor.schedules.length == 1) {
                $scope.is_scheduled = false; // Turn on that button
            }
            /* Shift all the following schedule's index down by one */
            for (var i = index + 1; i < $scope.fermentor.schedules.length; i++) {
                $scope.fermentor.schedules[i].index-=1;
            }
            $scope.fermentor.schedules.splice(index, 1);
        }

        $scope.update = function() {
            console.log("are probes changed yo? " + $scope.fermentor.probes_updated);
            console.log("is schedule changed yo? " + $scope.fermentor.schedule_updated);
            console.log("name is null? " + ($scope.fermentor.name == null) + "; name is ''? " + ($scope.fermentor.name == ''));

            console.log("$scope.fermentor = " + angular.toJson($scope.fermentor));

            $http.post('/fermentation/fermentor/change', angular.toJson($scope.fermentor))
            .success(function(data, status, headers, config) {
                console.log("its a success!");
                if ($scope.create) {
                    $scope.fermentor.id = data['fermentor_id']
                    $scope.fermentors.push($scope.fermentor); // Add created fermentor to array to display it in list
                    $scope.index_order[$scope.fermentor.id]=$scope.next_index; // Add new fermentor to index object
                    $scope.next_index += 1; // Increment index for next time in case user creates another fermentor
                } else if ($scope.edit) {
                    /* Determine which fermentor to pull out of the array via the index_order obj */
                    $scope.fermentors[$scope.index_order[$scope.fermentor.id]] = $scope.fermentor
                }

                $scope.reset(); // Change the create/edit new fermentor to null
                $scope.create = false;
                $scope.edit = false;

                console.log("data = " + data);
                console.log("status = " + status);
                console.log("headers = " + headers);
                console.log("config = " + config);

                $scope.save_error = false;
            })
            .error(function(data, status, headers, config) {
                console.log("its a failure NOOB");
                console.log("data = " + data);
                console.log("status = " + status);
                console.log("headers = " + headers);
                console.log("config = " + config);
                $scope.save_error = true;
            });
        }
        /* This needs to display some loading icon or something so the stupid end user doesn't think its broken */
        $scope.get_fermentors = function() {

            $http.get('/fermentation/fermentor/get')
            .success(function(data, status, headers, config) {
                $scope.fermentors = data; //JSON Array of fermentors

                $scope.index_order = {}; // This is used to pull the correct fermentor of of the array when user clicks Edit

                for (var i = 0; i < $scope.fermentors.length; i++) {

                    $scope.index_order[$scope.fermentors[i].id]=i; // Set the fermentor.id to the ith value

                    //$scope.fermentors[i].start_date = new Date($scope.fermentors[i].start_date);
                    //$scope.fermentors[i].end_begin_date = new Date($scope.fermentors[i].end_begin_date);
                    //$scope.fermentors[i].end_end_date = new Date($scope.fermentors[i].end_end_date);

                    for (var o = 0; o < $scope.fermentors[i].schedules.length; o++) {
                        $scope.fermentors[i].schedules[o].index = o; // This is for the add/remove schedule feature to keep them in order
                        //$scope.fermentors[i].schedules[o].dt = new Date($scope.fermentors[i].schedules[o].dt);

                    }
                }
                $scope.next_index = $scope.fermentors.length; // Increment the index for next time if user creates new fermentor


            }).
            error(function(data,status,headers,config) {
                console.log("its a failure NOOB");
            });
        }

        $scope.get_hosts = function() {
            $http.get('/fermentation/host/get')
            .success(function(data, status, headers, config) {
                $scope.hosts = data;
            }).
            error(function(data, status, headers, config) {
                console.log("noob host");
            });
        }

        $scope.get_probes = function() {
            $http.get('/fermentation/probe/get')
            .success(function(data, status, headers, config) {
                $scope.probes = data;
            }).
            error(function(data, status, headers, config) {
                console.log("noob probe");
            });
        }

        $scope.get_probe_types = function() {
            $http.get('/fermentation/probe_type/get')
            .success(function(data, status, headers, config) {
                $scope.probe_types = data;
            }).
            error(function(data, status, headers, config) {
                console.log("noob probe_types");
            });
        }

        $scope.get_fermwraps = function() {
            /* This is for the select box for the fermwrap pins */
            $http.get('/fermentation/fermwrap/get')
            .success(function(data, status, headers, config) {
                $scope.fermwraps = data;
            }).
            error(function(data, status, headers, config) {
                console.log("noob get_fermwraps");
            });
        }

        $scope.get_default_values = function() {
            /* This is for default values of new fermentor */
            $http.get('/fermentation/default/get')
            .success(function(data, status, headers, config) {
                $scope.default_host_id = data['default_host_id'];
                console.log("default host_id is " + $scope.default_host_id);
                $scope.default_temp = data['default_temp'];
                $scope.default_temp_differential = data['default_temp_differential']
                //$scope.default_today = new Date(data['default_today']);
                $scope.default_today = data['default_today'];
                //$scope.default_end_begin_date = new Date(data['default_end_begin_date']);
                $scope.default_end_begin_date = data['default_end_begin_date'];
                //$scope.default_end_end_date = new Date(data['default_end_end_date']);
                $scope.default_end_end_date = data['default_end_end_date'];
                $scope.default_material = data['default_material']

                console.log("default_today = " + $scope.default_today);

                $scope.reset();
            }).
            error(function(data, status, headers, config) {
                console.log("noob get_default_values");
            });
        }

        $scope.get_fermentors(); // Call the ajax to get an array of fermentors
        $scope.get_hosts();
        $scope.get_probes();
        $scope.get_probe_types();
        $scope.get_default_values();
        $scope.get_fermwraps();

        /* Master Fermentor is the base; but $scope.fermentor is the actual obj bound to the form for editing/creating a fermentor */
        // Right now this gets some values populating from python using the template system. Anything here with {} comes from python
        // I need to replace this with an ajax JSON call like I did with the fermentors

        $scope.reset = function() {
            /* Call this function whenever form to go back to null; e.g., save a fermentor */

            $scope.master = {}
            $scope.master.id = null;
            $scope.master.hostname = null;
            $scope.master.host_id = $scope.default_host_id;
            $scope.master.name = null;
            $scope.master.fermwrap = null;
            $scope.master.start_date = $scope.default_today;
            $scope.master.end_begin_date = $scope.default_end_begin_date;
            $scope.master.end_end_date = $scope.default_end_end_date;
            $scope.master.start_temp = $scope.default_temp;
            $scope.master.temp_differential = $scope.default_temp_differential;
            $scope.master.yeast = null;
            $scope.master.og = null;
            $scope.master.fg = null;
            $scope.master.material = $scope.default_material;
            $scope.master.probes = [{'file_name':null, 'type':'wort'}];
            $scope.master.schedules = [];

            //console.log("$scope.master.start_date = " + $scope.master.start_date);
            $scope.set_updated_to_false();

            $scope.fermentor = angular.copy($scope.master);
        };

        $scope.set_updated_to_false = function() {
            $scope.master.probes_updated = false;
            $scope.master.schedule_updated = false;
            $scope.master.fermwrap_updated = false;
        }







        $scope.create = false;
        $scope.edit = false;
        $scope.incomplete = false; // This should prevent the end user from submitting a form if he fucked up
        $scope.is_scheduled = false; // This is to show to initial add schedule button in case user doesnt want to add any temp schedules
        $scope.save_error = false; // This is for the span next to the save button if the AJAX returns an error



        /* Schedules need to be presented in order when the end user hits add or remove in the middle of a schedule */
        $scope.add_schedule = function(index) {
            /* Shift all the following schedule's index up by one */
            for (var i = index + 1; i < $scope.fermentor.schedules.length; i++) {
                $scope.fermentor.schedules[i].index += 1;
            }
            $scope.fermentor.schedules.splice(index + 1, 0, {'dt':null, 'temp':null, 'index':index+1});
        }
        $scope.remove_schedule = function(index) {
            //alert("index is " + index + " length is " + $scope.fermentor.schedules.length + "array is " + JSON.stringify($scope.fermentor.schedules));
            console.log("index = " + index);
            console.log("$scope.fermentor.schedules.length = " + $scope.fermentor.schedules.length);
            console.log("$scope.fermentor.schedules = " + angular.toJson($scope.fermentor.schedules));
            if ($scope.fermentor.schedules.length == 1) {
                $scope.is_scheduled = false; // Turn on that button
            }
            /* Shift all the following schedule's idnex down by one */
            for (var i = index + 1; i < $scope.fermentor.schedules.length; i++) {
                $scope.fermentor.schedules[i].index-=1;
            }
            $scope.fermentor.schedules.splice(index, 1);
        }
        $scope.increase_schedule = function(index) {
            for (var i = index; i < $scope.fermentor.schedules.length; i++) {
                var m = new moment($scope.fermentor.schedules[i].dt);
                m.add(12, 'hours');
                $scope.fermentor.schedules[i].dt = m.format('YYYY-MM-DDTHH:mm:ss');


            }
        }
        $scope.decrease_schedule = function(index) {
            for (var i = index; i < $scope.fermentor.schedules.length; i++) {
                var m = new moment($scope.fermentor.schedules[i].dt);
                m.subtract(12, 'hours');
                $scope.fermentor.schedules[i].dt = m.format('YYYY-MM-DDTHH:mm:ss');
            }
        }
        /* This is only for the initial add schedule button for a new fermentor */
        $scope.create_schedule = function() {

            // Append an empty schedule
            $scope.fermentor.schedules.push({'dt':null, 'temp':null, 'index':0});

            // Disable the inital add schedule button
            $scope.is_scheduled = true;
        }

        /* Unlike Schedules, Probes do not need to maintain any order in the UI */
        $scope.add_probe = function() {
            // No more than 3 probes per fermentor allowed
            if ($scope.fermentor.probes.length < 3) {
                $scope.fermentor.probes.push({'file_name':null, 'type':null});
            }
        }

        $scope.remove_probe = function() {
            // At least one probe for wort is required
            // This should implement some logic so the wort probe cannot be deleted off the UI
            if ($scope.fermentor.probes.length > 1) {
                $scope.fermentor.probes.pop();
            }
        }

        $scope.editFermentor = function(id) {
            /* This function handles both creating new fermentor and editing another fermentor depending on 'id' value */

            // Restset updated back to False because I'm editing/creating a different fermentor now
            $scope.set_updated_to_false();

            $scope.save_error = false;

            if (id == 'new') {
                // Creating a fermentor

                $scope.create = true;
                $scope.edit = false;
                $scope.incomplete = true;

                $scope.is_scheduled = false; // Not "is_scheduled" until punk ass end user clicks the first add schedule button

                $scope.reset();

                $scope.edit_original = null;

            } else {
                // Editing a fermentor

                $scope.create = false;
                $scope.edit = true;
                $scope.incomplete = false;

                // Pull the correct fermentor from the array bia the index_order dict
                var fermentor = $scope.fermentors[$scope.index_order[id]];


                $scope.fermentor.id = fermentor['id'];
                $scope.fermentor.hostname = fermentor['hostname'];
                $scope.fermentor.host_id = fermentor['host_id']
                $scope.fermentor.name = fermentor['name'];
                $scope.fermentor.fermwrap = fermentor['fermwrap']; // This is fermwrap pin
                $scope.fermentor.start_date = fermentor['start_date'];
                $scope.fermentor.end_begin_date = fermentor['end_begin_date'];
                $scope.fermentor.end_end_date = fermentor['end_end_date'];
                $scope.fermentor.start_temp = fermentor['start_temp'];
                $scope.fermentor.temp_differential = fermentor['temp_differential'];
                $scope.fermentor.yeast = fermentor['yeast'];
                $scope.fermentor.og = fermentor['og'];
                $scope.fermentor.fg = fermentor['fg'];
                $scope.fermentor.material = fermentor['material'];
                $scope.fermentor.probes = fermentor.probes;
                $scope.fermentor.schedules = fermentor.schedules;

                if ($scope.fermentor.schedules.length > 0) {
                    $scope.is_scheduled = true;
                } else {
                    $scope.is_scheduled = false;
                }

                $scope.edit_original = angular.copy($scope.fermentor); // Used to determine if probes or schedule has been updated

            }
        }

        $scope.$watch('fermentor.name', function() {$scope.watch_name();}); // This is not necessary
        $scope.$watch('fermentor.probes', function() {$scope.watch_probes();}, true);
        $scope.$watch('fermentor.schedules', function() {$scope.watch_schedule();}, true);
        $scope.$watch('fermentor.fermwrap', function() {$scope.watch_fermwrap();});

        $scope.watch_name = function() {
            /* This is not necessary */
            if ($scope.edit) {
                if ($scope.fermentor.name != $scope.edit_original.name) {
                    console.log("name differs");
                } else {
                    console.log("name not different");
                }
            }
        }


        $scope.watch_probes = function() {
            if ($scope.edit) {
                console.log("probe scope edit is true");
                if (angular.toJson($scope.fermentor.probes) != angular.toJson($scope.edit_original.probes)) {
                    $scope.fermentor.probes_updated = true;
                    console.log("probes differ");
                } else {
                    console.log("probes do not differ");
                }
            } else if ($scope.create) {
                // Back end will only create new probes if probes_updated == true
                $scope.fermentor.probes_updated = true;
                console.log("probes differ");
            }
        }

        $scope.watch_schedule = function() {
            if ($scope.edit) {
                console.log("scope edit is true");
                if (angular.toJson($scope.fermentor.schedules) != angular.toJson($scope.edit_original.schedules)) {
                    $scope.fermentor.schedule_updated = true;
                    console.log("schedules differ");
                } else {
                    console.log("schedules do not differ");
                }
            } else if ($scope.create && $scope.is_scheduled) {
                // Back end will only create new schedules if schedule_updated == true
                $scope.fermentor.schedule_updated = true;
                console.log("schedule updated");
            }
        }

        $scope.watch_fermwrap = function() {
            console.log("wathcing fermwrap");
            if ($scope.edit) {
                if ($scope.fermentor.fermwrap != $scope.edit_original.fermwrap) {
                    $scope.fermentor.fermwrap_updated = true;
                    console.log("fermwraps differ");
                } else {
                    console.log("fermwraps do not differ");
                }
            } else if ($scope.create) {
                $scope.fermentor.fermwrap_updated = true;
            }
        }



    }]);
</script>

</body>

</html>