<?php
class StatSorter {
	protected $column;
	protected $type;
	function __construct($column, $type="DESC") {
		$this->column = $column;
		$this->type = $type;
	}
	function sort($table) {
		usort($table, array($this, 'compare'));
		return $table;
	}
	function compare($a, $b) {
		if ($a[$this->column] == $b[$this->column]) {
			return 0;
		}
		if($this->type == "DESC"){	
			return ($a[$this->column] > $b[$this->column]) ? -1 : 1;
		} else {
			return ($a[$this->column] < $b[$this->column]) ? -1 : 1;
		}

	}
}
?>
