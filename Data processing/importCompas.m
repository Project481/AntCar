function [time, acc_x1, acc_y1, acc_z1, mag_x1, mag_y1, mag_z1] = importCompas(filename, dataLines)
%IMPORTFILE1 Import data from a text file
%  [TIME, ACC_X1, ACC_Y1, ACC_Z1, MAG_X1, MAG_Y1, MAG_Z1] =
%  IMPORTFILE1(FILENAME) reads data from text file FILENAME for the
%  default selection.  Returns the data as column vectors.
%
%  [TIME, ACC_X1, ACC_Y1, ACC_Z1, MAG_X1, MAG_Y1, MAG_Z1] =
%  IMPORTFILE1(FILE, DATALINES) reads data for the specified row
%  interval(s) of text file FILENAME. Specify DATALINES as a positive
%  scalar integer or a N-by-2 array of positive scalar integers for
%  dis-contiguous row intervals.
%
%  Example:
%  [time, acc_x1, acc_y1, acc_z1, mag_x1, mag_y1, mag_z1] = importfile1("D:\PFE\Test\Test0720\Recording 18-25-51 20.7.2020\Compas.csv", [2, Inf]);
%
%  See also READTABLE.
%
% Auto-generated by MATLAB on 21-Jul-2020 13:42:16

%% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [2, Inf];
end

%% Setup the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 7);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["time", "acc_x1", "acc_y1", "acc_z1", "mag_x1", "mag_y1", "mag_z1"];
opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
tbl = readtable(filename, opts);

%% Convert to output type
time = tbl.time;
acc_x1 = tbl.acc_x1;
acc_y1 = tbl.acc_y1;
acc_z1 = tbl.acc_z1;
mag_x1 = tbl.mag_x1;
mag_y1 = tbl.mag_y1;
mag_z1 = tbl.mag_z1;
end