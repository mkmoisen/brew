<HTML>
<HEAD>
    <link type="text/css" href="/static/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://code.jquery.com/jquery-latest.min.js"
        type="text/javascript"></script>
    <script>
        $(document).ready(function(){
            $('#right').click(function(){
                var lol = $('#available_pins').val();
                //alert(lol);
                $.each(lol, function(index, value) {
                    $('#selected_pins').append('<option value="' + value + '" selected>' + value + '</option>');
                });
            });

            $('#right_pump').click(function(){
                var lol = $('#available_pump_pin').val();
                //alert(lol);
                $.each(lol, function(index, value) {
                    $('#selected_pump_pin').append('<option value="' + value + '" selected>' + value + '</option>');
                });
            });

            $('#lol').click(function(){
                $('#selected_pins option').each(function() {
                    $(this).attr('selected', true);

                });
                //alert($(this).val() + " selected? " + $(this).attr('selected'));
                //alert($('#selected_pins').val());

                alert($('#step_index').val());
                $("#myform").submit();
            });

            $('#step_index').val(JSON.stringify(step_indexes));

        });

        var step_indexes = [0];

        var current_step_index = 0;

        var add_step = function(index) {
            current_step_index += 1;

            var splice_index = step_indexes.indexOf(index);

            //splice in new current_step_index after splice_index
            step_indexes.splice(splice_index + 1, 0, current_step_index);

            $('#step_index').val(JSON.stringify(step_indexes));


            var html_tr = '<TR id="step' + current_step_index + '"> \
                <TD> \
                    <INPUT name="step_name' + current_step_index + '" value="Mashout"/> \
                </TD> \
                <TD> \
                    <INPUT name="step_duration' + current_step_index + '" value="15"/> \
                </TD> \
                <TD> \
                    <INPUT name="step_temp' + current_step_index + '" value="168"/> \
                </TD> \
                <TD> \
                    <BUTTON id="add_step' + current_step_index + '" type="button" onclick="add_step(' + current_step_index + ');">Add Step</BUTTON> <BUTTON id="remove_step' + current_step_index + '" type="button" onclick="remove_step(' + current_step_index + ');">Remove Step</BUTTON> \
                </TD> \
            </TR>';

            $('#step' + index).after(html_tr);
        }

        var remove_step = function(index) {
            if (step_indexes.length != 1) {
                var remove_index = step_indexes.indexOf(index);
                step_indexes.splice(remove_index, 1);
                $('#step' + index).remove();
                $('#step_index').val(JSON.stringify(step_indexes));
            }
        }


    </script>


    <TITLE>HERMS Setup</TITLE>
</HEAD>
<Body>

    <FORM id="myform" action="/herms" method="post">
        <strong>Strike Temp Calculator</strong>
        <TABLE class="table">
            <TR>
                <TD>Room Temperature</TD>
                <TD>
                    <INPUT name="room_temp" type="text" value="70" />
                </TD>
            </TR>
            <TR>
                <TD>Water:Grist Ratio</TD>
                <TD>
                    <INPUT name="water_grist_ratio" type="text" value="1.25" />
                </TD>
            </TR>
        </TABLE>

        <strong>Probes</strong><BR />

        <TABLE class="table">
            <TR>
                <TD>HLT</TD>
                <TD>
                    <SELECT name="hlt_probe_file_name">
                        % for probe in probes:
                            <OPTION value="{{probe}}">{{probe}}</OPTION>
                        % end
                    </SELECT>
                </TD>
            </TR>
            <TR>
                <TD>Mashtun</TD>
                <TD>
                    <SELECT name="mashtun_probe_file_name">
                        % for probe in probes:
                            <OPTION value="{{probe}}">{{probe}}</OPTION>
                        % end
                    </SELECT>
                </TD>
            </TR>
        </TABLE>
        <BR />

        <STRONG>Heating Pins</STRONG><BR />

        <TABLE class="table">
            <TR>
                <TD>Available Pins</TD>
                <TD>Controls</TD>
                <TD>Used Pins</TD>
            </TR>
            <TR>
                <TD>
                    <SELECT id="available_pins" multiple size="6">
                        % for pin in pins:
                            <OPTION value="{{pin}}">{{pin}}</OPTION>
                        % end
                    </SELECT>
                </TD>
                <TD>
                    <button id="right" type="button">&#62;</button> <BR />
                    <BUTTON id="left" type="button">&#60;</BUTTON>
                </TD>
                <TD>
                    <SELECT id="selected_pins" name="selected_pins" multiple size="6">

                    </SELECT>
                </TD>
            </TR>

        </TABLE>
        <BR />

        <STRONG>Pump Pin</STRONG>
        <TABLE class="table">
            <TR>
                <TD>Available Pins</TD>
                <TD>Controls</TD>
                <TD>Used Pins</TD>
            </TR>
            <TR>
                <TD>
                    <SELECT id="available_pump_pin" multiple size="6">
                        % for pin in pins:
                            <OPTION value="{{pin}}">{{pin}}</OPTION>
                        % end
                    </SELECT>
                </TD>
                <TD>
                    <button id="right_pump" type="button">&#62;</button> <BR />
                    <BUTTON id="left_pump" type="button">&#60;</BUTTON>
                </TD>
                <TD>
                    <SELECT id="selected_pump_pin" name="selected_pump_pin" size="1">

                    </SELECT>
                </TD>
            </TR>
        </TABLE>

        <STRONG>Steps</STRONG>
        <TABLE id="step_table" class="table">
            <TR>
                <TD>Name</TD>
                <TD>Duration</TD>
                <TD>Temperature</TD>
                <TD></TD>
            </TR>
            <TR id="step0">
                <TD>
                    <INPUT name="step_name0" value="Sacc"/>
                </TD>
                <TD>
                    <INPUT name="step_duration0" />
                </TD>
                <TD>
                    <INPUT name="step_temp0"/>
                </TD>
                <TD>
                    <BUTTON id="add_step0" type="button" onclick="add_step(0);">Add Step</BUTTON> <BUTTON id="remove_step0" onclick="remove_step(0);" type="button">Remove Step</BUTTON>
                </TD>
            </TR>
        </TABLE>

        <BR/>

        <input name="step_index" id="step_index" type="hidden" />

        <BUTTON id="lol" type="button">Submit</BUTTON>
    </FORM>
</Body>
</HTML>