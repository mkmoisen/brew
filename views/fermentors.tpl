<html>
<head>
	<title>Fermentors</title>
	<!-- Bootstrap -->
    <link type="text/css" href="/static/css/bootstrap.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>

    <script src= "http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.min.js"></script>
<script>
        $(document).ready(function(){
           

            $('#lol').click(function(){

                alert($('#schedule_index').val());
                $("#myform").submit();
            });

            $('#schedule_index').val(JSON.stringify(schedule_indexes));

        });

        var schedule_indexes = [0];

        var current_schedule_index = 0;

        var add_schedule = function(index) {
            current_schedule_index += 1;

            var splice_index = schedule_indexes.indexOf(index);

            //splice in new current_schedule_index after splice_index
            schedule_indexes.splice(splice_index + 1, 0, current_schedule_index);

            $('#schedule_index').val(JSON.stringify(schedule_indexes));


            var html_tr = '<TR id="schedule' + current_schedule_index + '"> \
                <TD> \
                    <INPUT name="schedule_dt' + current_schedule_index + '" /> \
                </TD> \
                <TD> \
                    <INPUT name="schedule_temp' + current_schedule_index + '" /> \
                </TD> \
                <TD> \
                    <BUTTON id="add_schedule' + current_schedule_index + '" type="button" onclick="add_schedule(' + current_schedule_index + ');">Add schedule</BUTTON> <BUTTON id="remove_schedule' + current_schedule_index + '" type="button" onclick="remove_schedule(' + current_schedule_index + ');">Remove schedule</BUTTON> \
                </TD> \
            </TR>';

            $('#schedule' + index).after(html_tr);
        }

        var remove_schedule = function(index) {
            if (schedule_indexes.length != 1) {
                var remove_index = schedule_indexes.indexOf(index);
                schedule_indexes.splice(remove_index, 1);
                $('#schedule' + index).remove();
                $('#schedule_index').val(JSON.stringify(schedule_indexes));
            }
        }


    </script>
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
                                        <TD><SPAN ng-bins="probe.type"></SPAN></TD>
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
                    <SELECT ng-model="fermentor.host_id">
                        % for host in hosts:
                            <OPTION value="{{host.id}}" >{{host.hostname}}</OPTION>
                        % end
                    </SELECT>
                </TD>
                <TD><INPUT ng-model="fermentor.name" type="text" /></TD>
                <TD>
                    <SELECT ng-model="fermentor.fermwrap">
                        % for fermwrap in fermwraps:
                            <OPTION value="{{fermwrap}}">{{fermwrap}}</OPTION>
                        % end
                    </SELECT>
                </TD>
                <TD><INPUT ng-model="fermentor.start_date" type="text" name="start_date" /></TD>
                <TD><INPUT ng-model="fermentor.end_begin_date" type="text" name="end_begin_date"  /></TD>
                <TD><INPUT ng-model="fermentor.end_end_date" type="text" name="end_end_date" /></TD>
                <TD><INPUT ng-model="fermentor.start_temp" type="text" name="start_temp" /></TD>
                <TD><INPUT ng-model="fermentor.temp_differential" type="text" name="temp_differential" /></TD>
                <TD><INPUT ng-model="fermentor.yeast" type="text" name="yeast" /></TD>
                <TD><INPUT ng-model="fermentor.og" type="text" name="og" /></TD>
                <TD><INPUT ng-model="fermentor.fg" type="text" name="fg" /></TD>
                <TD><INPUT ng_model="fermentor.material" type="text" name="material" value="Glass" /></TD>

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
                    <SELECT ng-model="probe.file_name">
                        % for probe in probes:
                            <OPTION value="{{probe}}">{{probe}}</OPTION>
                        % end
                    </SELECT>
                </TD>
                <TD>
                    <SELECT ng-model="probe.type">
                        % for probe_type in probe_types:
                            <OPTION value="{{probe_type}}">{{probe_type}}</OPTION>
                        % end
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
                </TD>
            </TR>

        </TBODY>
    </TABLE>


    <input name="schedule_index" id="schedule_index" type="hidden" />

    </FORM>

<HR />

<BUTTON ng-click="update()" class="btn btn-success">
    <SPAN class="glyphicon glyphicon-save"></SPAN> Save Changes
</BUTTON>

</DIV>

</DIV>



<script>
    angular.module('myApp', []).controller('fermentorController', ['$scope',  '$http', function($scope, $http) {

        $scope.update = function() {
            console.log("are probes changed yo? " + $scope.fermentor.probes_updated);
            console.log("is schedule changed yo? " + $scope.fermentor.schedule_updated);
            console.log("name is null? " + ($scope.fermentor.name == null) + "; name is ''? " + ($scope.fermentor.name == ''));
            $http.post('/fermentor/change', angular.toJson($scope.fermentor));
        }

        $scope.master = {}
        $scope.master.id = null;
        $scope.master.hostname = '{{hostname}}';
        $scope.master.host_id = null;
        $scope.master.name = null;
        $scope.master.fermwrap = null;
        $scope.master.start_date = '{{today}}';
        $scope.master.end_begin_date = '{{four_weeks_later}}';
        $scope.master.end_end_date = '{{six_weeks_later}}';
        $scope.master.start_temp = null;
        $scope.master.temp_differential = null;
        $scope.master.yeast = null;
        $scope.master.og = null;
        $scope.master.fg = null;
        $scope.master.material = 'Glass';
        $scope.master.probes = [{'file_name':null, 'type':'wort'}];
        $scope.master.schedules = [{'dt':null, 'temp':null, 'index':0}];

        $scope.master.probes_updated = false
        $scope.master.schedule_updated = false

        $scope.reset = function() {
            $scope.fermentor = angular.copy($scope.master);
        };
        $scope.reset();

        $scope.create = false;
        $scope.edit = false;
        $scope.incomplete = false;



        % index = 0
        % index_order = {}

        $scope.fermentors = [
            % for fermentor in fermentors:
                % index_order[fermentor.id] = index
                % index += 1
                {
                    id:{{fermentor.id}},
                    hostname:'{{fermentor.host.hostname}}',
                    host_id:{{fermentor.host.id}},
                    name:'{{fermentor.name}}',
                    % for fermwrap in fermentor.fermentor_fermwraps:
                    fermwrap:{{fermwrap.pin}},
                    % end
                    start_date:'{{fermentor.start_date}}',
                    end_begin_date:'{{fermentor.end_begin_date}}',
                    end_end_date:'{{fermentor.end_end_date}}',
                    start_temp:{{fermentor.start_temp}},
                    temp_differential:{{fermentor.temp_differential}},
                    yeast:'{{fermentor.yeast}}',
                    og:{{fermentor.og}},
                    fg:{{!'null' if fermentor.fg is None else fermentor.fg}},
                    material:'{{fermentor.material}}',
                    probes:[
                        % for probe in fermentor.fermentor_probes:
                            {
                                file_name:'{{probe.file_name}}',
                                type:'{{probe.type}}'
                            },
                        % end
                    ],schedules:[
                        % schedule_index = 0
                        % for schedule in fermentor.fermentor_schedules:
                            {
                                dt:'{{schedule.dt}}',
                                temp:{{schedule.temp}},
                                index:{{schedule_index}}
                            },
                            % schedule_index += 1
                        % end
                    ],
                },
            % end
        ];

        $scope.index_order = {{index_order}};

        $scope.add_schedule = function(index) {
            for (i = index + 1; i < $scope.fermentor.schedules.length; i++) {
                $scope.fermentor.schedules[i].index += 1;
            }
            $scope.fermentor.schedules.splice(index + 1, 0, {'dt':null, 'temp':null, 'index':index+1});
        }
        $scope.remove_schedule = function(index) {
            //alert("index is " + index + " length is " + $scope.fermentor.schedules.length + "array is " + JSON.stringify($scope.fermentor.schedules));
            if ($scope.fermentor.schedules.length == 1) {
                //alert("block");
                return;
            }
            $scope.fermentor.schedules.splice(index, 1);
        }

        $scope.add_probe = function() {
            if ($scope.fermentor.probes.length < 3) {
                $scope.fermentor.probes.push({'file_name':null, 'type':null});
            }
        }

        $scope.remove_probe = function() {
            if ($scope.fermentor.probes.length > 1) {
                $scope.fermentor.probes.pop();
            }
        }

        $scope.editFermentor = function(id) {

            if (id == 'new') {
                $scope.create = true;
                $scope.edit = false;
                $scope.incomplete = true;

                $scope.reset();

            } else {
                $scope.create = false;
                $scope.edit = true;
                $scope.incomplete = false;

                var fermentor = $scope.fermentors[$scope.index_order[id]];


                $scope.fermentor.id = fermentor['id'];
                $scope.fermentor.hostname = fermentor['hostname'];
                $scope.fermentor.host_id = fermentor['host_id']
                $scope.fermentor.name = fermentor['name'];
                $scope.fermentor.fermwrap = fermentor['fermwrap'];
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

                $scope.edit_original = angular.copy($scope.fermentor);

            }
        }

        $scope.$watch('fermentor.probes', function() {$scope.watch_probes();}, true);
        $scope.$watch('fermentor.schedules', function() {$scope.watch_schedule();}, true);
        $scope.$watch('fermentor.name', function() {$scope.watch_name();});


        $scope.watch_name = function() {
            console.log("name watch");
            if ($scope.fermentor.name != $scope.edit_original.name) {
                console.log("name differs");
            } else {
                console.log("name not different");
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
            }
        }



    }]);
</script>

</body>

</html>