import CameraView from "../components/CameraView";
import StatusPanel from "../components/StatusPanel";
import ControlPanel from "../components/ControlPanel";

const Dashboard = () => {
  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Driver Drowsiness Detection</h1>
      <CameraView />
      <StatusPanel />
      <ControlPanel />
    </div>
  );
};

export default Dashboard;
