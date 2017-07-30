#include "Node.h"

namespace {{cookiecutter.project_module_name}} {

void Node::begin() {
  config_.set_buffer(get_buffer());
  config_.validator_.set_node(*this);
  config_.reset();
  config_.load();

  state_.set_buffer(get_buffer());
  state_.validator_.set_node(*this);
  // XXX Reset all state fields to default values (if available).
  state_.reset();
  // XXX Must explicitly mark all state fields as present to validate them.
  // state_._.has_<fieldname> = true;

  // Validate state to trigger on-changed handling for state fields that are
  // set (which initializes the state to the default values supplied in the
  // state protocol buffer definition).
  state_.validate();

  Serial.begin({{cookiecutter.hardware_baudrate}});

  // If we have a valid i2c address (i.e., if Wire.begin() was called)
  if (config_._.i2c_address > 0) {
    // set the i2c clock
    Wire.setClock({{cookiecutter.hardware_i2c_clock_rate}});
  }
}

}  // namespace {{cookiecutter.project_module_name}}
